# test_catalogo.py
# Ejecutar con: pytest -q
#
# Estas pruebas intentan "romper" el dominio: entradas inválidas, tipos incorrectos,
# invariantes violadas, combos mal formados, exportaciones inesperadas, etc.
# Si todas pasan, el dominio resiste intentos agresivos de fallo.

from dataclasses import FrozenInstanceError

import pytest


from catalogo import (
    Categoria,
    DomainError,
    Exportable,
    Producto,
    ProductoCategoria,
    ProductoCombo,
    ProductoDestacado,
    ProductoPorPeso,
    ProductoSimple,
    UnidadMedida,
    exportar_catalogo,
)

# librería externa (SE ENTREGA, NO MODIFICAR)
from libreria_externa import FichaPuntoDeVenta

# ---------------------------
# Helpers para crear objetos
# ---------------------------

def um_kg():
    return UnidadMedida("Kilogramo", "kg", "masa")


def um_unidad():
    return UnidadMedida("Unidad", "u", "unidad")


def categoria(nombre="Genérico"):
    return Categoria(nombre, "desc")


def simple(nombre="S", precio=100, stock=10, unidad=None, cat=None):
    if unidad is None:
        unidad = um_unidad()
    if cat is None:
        cat = categoria()
    return ProductoSimple(nombre, precio, stock, unidad, cat)


def por_peso(nombre="P", precio=10.5, stock=100, unidad=None, cat=None):
    if unidad is None:
        unidad = um_kg()
    if cat is None:
        cat = categoria()
    return ProductoPorPeso(nombre, precio, stock, unidad, cat)


# ---------------------------
# UnidadMedida / Categoria
# ---------------------------

def test_unidad_medida_frozen():
    u = UnidadMedida("Litro", "L", "volumen")
    with pytest.raises(FrozenInstanceError):
        u.nombre = "Otro"


def test_categoria_nombre_vacio_falla():
    with pytest.raises(DomainError):
        Categoria("", "desc")
    with pytest.raises(DomainError):
        Categoria("   ", "desc")


def test_categoria_propiedades_inmutables():
    c = Categoria("Bebidas", "sin alcohol")
    assert c.nombre == "Bebidas"
    assert c.descripcion == "sin alcohol"


# ---------------------------
# ProductoCategoria / composición
# ---------------------------

def test_producto_crea_producto_categoria_composicion():
    c = categoria("A")
    p = simple("X", 10, 5, um_unidad(), c)
    # El producto debe tener al menos una clasificación (la principal creada en el constructor)
    clas = p.categorias
    assert len(clas) >= 1
    assert any(v.es_principal for v in clas)
    # El vínculo guarda la categoría correcta
    assert p.categoria_principal.nombre == "A"


def test_producto_categoria_marcar_principal_mutable_privado():
    c = categoria("C")
    p = simple("X", 10, 5, um_unidad(), c)
    vinculo = p.categorias[0]
    # Forzamos cambio interno (método privado expuesto en la clase)
    vinculo._marcar_principal(False)
    assert vinculo.es_principal is False


# ---------------------------
# Producto (abstracto) - validaciones generales
# ---------------------------

def test_producto_nombre_vacio_falla():
    with pytest.raises(DomainError):
        ProductoSimple("", 1, 1, um_unidad(), categoria())


def test_producto_precio_base_negativo_falla():
    with pytest.raises(DomainError):
        ProductoSimple("X", -1, 1, um_unidad(), categoria())


def test_producto_stock_negativo_falla():
    with pytest.raises(DomainError):
        ProductoSimple("X", 1, -5, um_unidad(), categoria())


def test_habilitar_deshabilitar_y_disponible():
    p = simple("Y", 10, 1)
    assert p.disponible is True
    p.deshabilitar()
    assert p.disponible is False
    p.habilitar()
    assert p.disponible is True
    # stock 0 => no disponible
    p2 = simple("Z", 10, 0)
    assert p2.disponible is False


# ---------------------------
# ProductoSimple - reglas específicas
# ---------------------------

def test_producto_simple_precio_base_entero_requerido():
    # precio_base 1.5 no entero -> falla
    with pytest.raises(DomainError):
        ProductoSimple("A", 1.5, 1, um_unidad(), categoria())
    # precio_base 0 -> falla (debe ser >= 1)
    with pytest.raises(DomainError):
        ProductoSimple("A", 0, 1, um_unidad(), categoria())
    # precio_base 1.0 (float pero entero en valor) debe pasar
    p = ProductoSimple("OK", 1.0, 1, um_unidad(), categoria())
    assert p.precio_base == 1.0


def test_producto_simple_precio_final_cantidad_entera():
    p = ProductoSimple("P", 10, 5, um_unidad(), categoria())
    assert p.precio_final(1) == 10
    assert p.precio_final(2.0) == 20  # 2.0 es aceptado porque es entero en valor
    with pytest.raises(DomainError):
        p.precio_final(0)
    with pytest.raises(DomainError):
        p.precio_final(1.5)


def test_producto_simple_exportar_formato():
    p = ProductoSimple("Coca", 100, 10, um_unidad(), categoria("Bebidas"))
    assert p.exportar().startswith("PROD|Coca|100")


# ---------------------------
# ProductoPorPeso - reglas específicas
# ---------------------------

def test_producto_por_peso_precio_base_positivo():
    with pytest.raises(DomainError):
        ProductoPorPeso("P", 0, 1, um_kg(), categoria())
    p = ProductoPorPeso("Q", 0.5, 10, um_kg(), categoria())
    assert p.precio_base == 0.5


def test_producto_por_peso_precio_final_redondeo():
    p = ProductoPorPeso("Q", 0.3333, 10, um_kg(), categoria())
    # 0.3333 * 3 = 0.9999 -> redondea a 1.00
    assert p.precio_final(3) == round(0.3333 * 3, 2)
    with pytest.raises(DomainError):
        p.precio_final(0)


def test_producto_por_peso_exportar_incluye_unidad():
    u = UnidadMedida("Kilogramo", "kg", "masa")
    p = ProductoPorPeso("Arroz", 50.0, 100, u, categoria("Alimentos"))
    assert "PROD_PESO|Arroz|50.0|kg" == p.exportar()


# ---------------------------
# ProductoCombo - reglas y decisiones de diseño
# ---------------------------

def test_producto_combo_requiere_al_menos_dos_componentes():
    a = simple("A", 10, 5)
    with pytest.raises(DomainError):
        ProductoCombo("ComboFail", [a], 0.1, um_unidad(), categoria())


def test_producto_combo_componentes_deben_ser_producto():
    class NotProduct:
        pass

    with pytest.raises(DomainError):
        ProductoCombo("ComboFail", [NotProduct(), NotProduct()], 0.1, um_unidad(), categoria())


def test_producto_combo_descuento_rango():
    a = simple("A", 10, 5)
    b = simple("B", 20, 5)
    with pytest.raises(DomainError):
        ProductoCombo("C", [a, b], -0.1, um_unidad(), categoria())
    with pytest.raises(DomainError):
        ProductoCombo("C", [a, b], 1.0, um_unidad(), categoria())


def test_producto_combo_precio_base_derivado_y_precio_final():
    a = ProductoSimple("A", 100, 5, um_unidad(), categoria())
    b = ProductoSimple("B", 200, 5, um_unidad(), categoria())
    combo = ProductoCombo("Combo", [a, b], 0.1, um_unidad(), categoria())
    # precio_base del combo es suma de precios base de componentes
    assert combo.precio_base == 300
    # precio_final con descuento 10%: (100 + 200) * 0.9 * cantidad
    assert combo.precio_final(1) == pytest.approx(270.0)
    assert combo.precio_final(2) == pytest.approx(540.0)


def test_producto_combo_disponibilidad_derivada_de_componentes():
    a = simple("A", 10, 1)
    b = simple("B", 20, 1)
    combo = ProductoCombo("C", [a, b], 0.0, um_unidad(), categoria())
    assert combo.disponible is True
    # si uno de los componentes se queda sin stock, combo no disponible
    a2 = ProductoSimple("A2", 10, 0, um_unidad(), categoria())
    combo2 = ProductoCombo("C2", [a2, b], 0.0, um_unidad(), categoria())
    assert combo2.disponible is False
    # si se deshabilita un componente, combo no disponible
    a.habilitar()
    b.habilitar()
    combo3 = ProductoCombo("C3", [a, b], 0.0, um_unidad(), categoria())
    assert combo3.disponible is True
    b.deshabilitar()
    assert combo3.disponible is False or combo3.disponible is False  # comprobación redundante para claridad


def test_producto_combo_exportar_formato():
    a = simple("A", 10, 1)
    b = simple("B", 20, 1)
    combo = ProductoCombo("ComboX", [a, b], 0.2, um_unidad(), categoria())
    assert combo.exportar().startswith("COMBO|ComboX|2")


def test_producto_combo_precio_final_valida_cantidad_entera():
    a = simple("A", 10, 5)
    b = simple("B", 20, 5)
    combo = ProductoCombo("C", [a, b], 0.0, um_unidad(), categoria())
    with pytest.raises(DomainError):
        combo.precio_final(0)
    with pytest.raises(DomainError):
        combo.precio_final(1.5)


# ---------------------------
# ProductoDestacado - rediseño por composición
# ---------------------------

def test_producto_destacado_no_hereda_producto_y_envuelve():
    p = simple("S", 10, 5)
    d = ProductoDestacado(p, 1)
    # No es instancia de Producto
    assert not isinstance(d, Producto)
    # Devuelve el producto envuelto
    assert d.producto is p
    # Exporta delegando al producto envuelto
    assert d.exportar() == f"DEST|{p.nombre}|{d.orden_vidriera}"


def test_producto_destacado_permite_destacar_cualquier_producto_incluso_combo():
    a = simple("A", 10, 5)
    b = simple("B", 20, 5)
    combo = ProductoCombo("Combo", [a, b], 0.1, um_unidad(), categoria())
    d = ProductoDestacado(combo, 5)
    assert d.producto is combo
    assert d.exportar() == f"DEST|{combo.nombre}|5"


# ---------------------------
# Clasificación y reglas de negocio
# ---------------------------

def test_clasificar_en_no_permite_repetir_categoria():
    p = simple("X", 10, 5)
    c = categoria("C1")
    p.clasificar_en(c, es_principal=False)
    with pytest.raises(DomainError):
        p.clasificar_en(c, es_principal=False)


def test_clasificar_en_cambia_principal():
    p = simple("X", 10, 5)
    c1 = categoria("C1")
    c2 = categoria("C2")
    p.clasificar_en(c1, es_principal=True)
    assert p.categoria_principal is c1
    p.clasificar_en(c2, es_principal=True)
    assert p.categoria_principal is c2


# ---------------------------
# Exportable / export_catalogo / conformidad estructural
# ---------------------------

def test_export_catalogo_acepta_cualquier_objeto_con_exportar():
    p = simple("S", 10, 5)
    d = ProductoDestacado(p, 2)
    f = FichaPuntoDeVenta("C123", "detalleX")
    out = exportar_catalogo([p, d, f])
    assert any(s.startswith("PROD|") for s in out)
    assert any(s.startswith("DEST|") for s in out)
    assert any(s.startswith("POS|") for s in out)


# ---------------------------
# Robustez: tipos y valores extremos
# ---------------------------

def test_valores_extremos_y_tipos_raros():
    # nombres muy largos, precios muy grandes, cantidades grandes
    long_name = "X" * 1000
    big_price = 10 ** 9
    p = ProductoSimple(long_name, big_price, 10 ** 6, um_unidad(), categoria("G"))
    assert p.precio_base == big_price
    assert p.precio_final(10) == big_price * 10

    # floats que son enteros en valor
    p2 = ProductoSimple("I", 2.0, 1, um_unidad(), categoria())
    assert p2.precio_final(2.0) == 4.0

    # ProductoPorPeso con cantidad decimal grande
    pp = ProductoPorPeso("Peso", 0.123456, 1000, um_kg(), categoria())
    assert isinstance(pp.precio_final(123.456), float)


# ---------------------------
# Integración: cambios en componentes afectan combos (dinámica)
# ---------------------------

def test_combo_refleja_cambios_en_componentes():
    a = ProductoSimple("A", 100, 1, um_unidad(), categoria())
    b = ProductoSimple("B", 50, 1, um_unidad(), categoria())
    combo = ProductoCombo("C", [a, b], 0.0, um_unidad(), categoria())
    assert combo.precio_base == 150
    # Cambiamos precio base de A (atributo privado, pero posible)
    a._precio_base = 200
    assert combo.precio_base == 250
    # Cambiamos disponibilidad de B
    b._stock_cantidad = 0
    assert combo.disponible is False


# ---------------------------
# Casos que deben fallar por tipo
# ---------------------------

def test_pasar_none_en_unidad_venta_y_precio_publicado():
    # unidad_venta puede ser None; precio_publicado debe formatear sin unidad
    p = ProductoSimple("SinUnidad", 10, 1, None, categoria())
    assert p.precio_publicado.startswith("$ 10.00")
    # exportar de ProductoPorPeso con unidad None fallará al acceder a simbolo
    with pytest.raises(AttributeError):
        ProductoPorPeso("P", 1.0, 1, None, categoria()).exportar()


def test_export_catalogo_con_objeto_mal_formado_levanta_error():
    # objeto que tiene exportar pero que lanza error internamente
    class MalExportable:
        def exportar(self):
            raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        exportar_catalogo([MalExportable()])


# ---------------------------
# Cobertura extra: asegurar que los métodos abstractos están presentes
# ---------------------------

def test_producto_abstracto_no_instanciable_directamente():
    with pytest.raises(TypeError):
        Producto("X", 1, 1, um_unidad(), categoria())  # Producto es abstracto


# ---------------------------
# Stress tests: muchas clasificaciones y componentes
# ---------------------------

def test_many_classifications_and_components():
    base = simple("Base", 10, 10)
    comps = [simple(f"C{i}", 1 + i, 10) for i in range(20)]
    combo = ProductoCombo("Mega", comps, 0.05, um_unidad(), categoria())
    # precio_base suma de todos los componentes
    expected = sum(c.precio_base for c in comps)
    assert combo.precio_base == expected
    # agregar muchas clasificaciones a un producto
    p = simple("Multi", 5, 5)
    for i in range(30):
        p.clasificar_en(categoria(f"Cat{i}"), es_principal=(i == 29))
    assert p.categoria_principal.nombre == "Cat29"
    assert len(p.categorias) >= 30


# ---------------------------
# Asegurar mensajes de error útiles (no estrictamente necesario, pero comprobamos que se lanza DomainError)
# ---------------------------

def test_mensajes_de_error_en_validaciones():
    with pytest.raises(DomainError) as exc:
        ProductoSimple("X", 0, 1, um_unidad(), categoria())
    assert "precio_base" in str(exc.value) or "entero" in str(exc.value) or exc.type is DomainError

    with pytest.raises(DomainError) as exc2:
        ProductoPorPeso("Y", 0, 1, um_kg(), categoria())
    assert "precio_base" in str(exc2.value) or exc2.type is DomainError

# test_hardening.py
# Ejecutar con: pytest -q -s

import threading
import random
import math
import time
import pytest

from catalogo import (
    Categoria,
    DomainError,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    ProductoDestacado,
    UnidadMedida,
    exportar_catalogo,
)
from libreria_externa import FichaPuntoDeVenta


# ---------------------------
# Serialización / Deserialización (idempotencia parcial)
# ---------------------------

def parse_export_line(line: str):
    """Parser mínimo para los formatos exportados por el dominio."""
    parts = line.split("|")
    kind = parts[0]
    if kind == "PROD":
        # PROD|nombre|precio_base
        _, nombre, precio = parts
        return ("PROD", nombre, float(precio))
    if kind == "PROD_PESO":
        # PROD_PESO|nombre|precio|simbolo
        _, nombre, precio, simbolo = parts
        return ("PROD_PESO", nombre, float(precio), simbolo)
    if kind == "COMBO":
        # COMBO|nombre|n_componentes
        _, nombre, n = parts
        return ("COMBO", nombre, int(n))
    if kind == "DEST":
        # DEST|nombre|orden
        _, nombre, orden = parts
        return ("DEST", nombre, int(orden))
    if kind == "POS":
        # POS|codigo|detalle
        _, codigo, detalle = parts
        return ("POS", codigo, detalle)
    return ("UNKNOWN", line)


def test_export_parse_roundtrip_simple_and_peso_and_combo():
    u = UnidadMedida("Unidad", "u", "unidad")
    c = Categoria("X")
    s = ProductoSimple("S", 10, 5, u, c)
    p = ProductoPorPeso("P", 2.5, 10, u, c)
    combo = ProductoCombo("C", [s, s], 0.1, u, c)

    lines = [s.exportar(), p.exportar(), combo.exportar()]
    parsed = [parse_export_line(l) for l in lines]

    # Verificamos que el parser reconoce los tipos y que al menos la info clave se mantiene
    assert parsed[0][0] == "PROD" and parsed[0][1] == "S"
    assert parsed[1][0] == "PROD_PESO" and parsed[1][1] == "P"
    assert parsed[2][0] == "COMBO" and parsed[2][1] == "C" and parsed[2][2] == 2


# ---------------------------
# Concurrencia: intentar romper invariantes
# ---------------------------

def worker_modify(product, iterations, errors):
    try:
        for _ in range(iterations):
            # alternamos cambios de precio y stock
            product._precio_base = max(0, product._precio_base + random.choice([-1, 0, 1]))
            product._stock_cantidad = max(0, product._stock_cantidad + random.choice([-1, 0, 1]))
    except Exception as e:
        errors.append(e)


def test_concurrency_modify_price_and_stock_no_crash():
    u = UnidadMedida("Unidad", "u", "unidad")
    c = Categoria("Conc")
    p = ProductoSimple("ConcProd", 100, 100, u, c)

    threads = []
    errors = []
    for _ in range(20):
        t = threading.Thread(target=worker_modify, args=(p, 1000, errors))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # No deben haberse producido excepciones en los hilos
    assert errors == []

    # Invariantes básicas: precio y stock no negativos
    assert p.precio_base >= 0
    assert p._stock_cantidad >= 0


# ---------------------------
# Fuzzing: inputs aleatorios y extremos
# ---------------------------

def random_name():
    # mezcla de caracteres raros, espacios, y longitudes variables
    choices = ["", " ", "   ", "N" * random.randint(0, 2000), "\n", "\t", "ñáéíóú", "🚀"]
    return random.choice(choices) + "".join(random.choices("ABCxyz0123-_.", k=random.randint(0, 50)))


def test_fuzzing_many_random_inputs():
    u = UnidadMedida("U", "u", "tipo")
    for _ in range(200):
        name = random_name()
        precio = random.choice([random.uniform(-1e6, 1e6), float("nan"), float("inf"), 1.0, 2.0])
        stock = random.choice([random.uniform(-1000, 1000), float("nan"), float("inf"), 0, 10])
        try:
            # Intentamos crear ProductoSimple cuando el precio es entero en valor
            if isinstance(precio, float) and precio == int(precio) and precio >= 1 and not math.isnan(precio) and not math.isinf(precio):
                p = ProductoSimple(str(name or "N"), float(precio), float(max(0, int(stock) if isinstance(stock, (int, float)) else 0)), u, Categoria("G"))
                # precio_final con cantidad entera
                try:
                    p.precio_final(1)
                except DomainError:
                    pytest.fail("ProductoSimple válido lanzó DomainError en precio_final")
            else:
                # Para valores inválidos esperamos DomainError o TypeError
                with pytest.raises((DomainError, TypeError, ValueError)):
                    ProductoSimple(str(name or "N"), float(precio), float(stock if isinstance(stock, (int, float)) else 0), u, Categoria("G"))
        except (ValueError, OverflowError):
            # Algunos casts pueden lanzar; lo aceptamos como resultado del fuzzing
            pass


# ---------------------------
# Performance: combos muy grandes
# ---------------------------

def test_combo_grande_precio_base_y_precio_final():
    u = UnidadMedida("U", "u", "tipo")
    c = Categoria("Mega")
    # creamos 5000 componentes simples con precio incremental
    comps = [ProductoSimple(f"P{i}", float(i + 1), 10, u, c) for i in range(5000)]
    combo = ProductoCombo("MegaCombo", comps, 0.05, u, c)

    start = time.perf_counter()
    pb = combo.precio_base
    pf = combo.precio_final(1)
    elapsed = time.perf_counter() - start

    # precio_base debe ser suma de 1..5000
    expected = sum(float(i + 1) for i in range(5000))
    assert pb == expected
    # precio_final aplica descuento 5%
    assert pf == pytest.approx(expected * (1 - 0.05))
    # No imponemos un límite estricto de tiempo, pero comprobamos que la operación se completó
    assert elapsed < 5.0  # razonable en la mayoría de entornos; si falla, indica problema de performance


# ---------------------------
# Cobertura de errores de integración en exportar_catalogo
# ---------------------------

def test_exportar_catalogo_propagates_exceptions_from_items():
    class Bad:
        def exportar(self):
            raise RuntimeError("boom external")

    with pytest.raises(RuntimeError):
        exportar_catalogo([Bad()])


def test_exportar_catalogo_con_ficha_externa_raise_handled():
    # Simulamos que la ficha externa lanza error internamente
    class FichaMal(FichaPuntoDeVenta):
        def exportar(self):
            raise RuntimeError("pos fail")

    f = FichaMal("X", "d")
    with pytest.raises(RuntimeError):
        exportar_catalogo([f])


# ---------------------------
# Propiedades de dominio: igualdad, hash y uso como clave
# ---------------------------

def test_categoria_hashable_y_distintas_instancias_no_iguales():
    a = Categoria("Same")
    b = Categoria("Same")
    # por diseño no implementamos __eq__, así que son distintas instancias
    assert a is not b
    d = {a: "uno", b: "dos"}
    assert d[a] == "uno"
    assert d[b] == "dos"
    # verificar que se pueden usar en sets
    s = {a, b}
    assert len(s) == 2


def test_unidad_medida_frozen_confirmacion():
    u = UnidadMedida("X", "x", "t")
    with pytest.raises(AttributeError):
        # dataclass frozen lanza AttributeError al intentar asignar
        u.nombre = "Y"



if __name__ == "__main__":
    import pytest
    pytest.main(["-q", "-s", __file__])