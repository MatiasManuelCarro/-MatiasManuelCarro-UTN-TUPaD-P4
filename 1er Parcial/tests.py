from catalogo_old import (
    Categoria,
    DomainError,
    Producto,
    ProductoCombo,
    ProductoDestacado,
    ProductoPorPeso,
    ProductoSimple,
    UnidadMedida,
)
from libreria_externa import FichaPuntoDeVenta

# ============================
# PRUEBAS COMPLETAS DEL MODELO
# ============================

print("\n=== PRUEBA 1: Falla temprana al instanciar Producto (abstracta) ===")
try:
    p = Producto(
        nombre="Test",
        precio_base=100,
        stock_cantidad=10,
        unidad_venta=None,
        categoria_principal=Categoria("Test"),
        habilitado=True,
    )
except TypeError as e:
    print("OK:", e)


print("\n=== PRUEBA 2: Falla temprana al instanciar subclase incompleta ===")
class ProductoIncompleto(Producto):
    pass  # NO implementa precio_final()

try:
    x = ProductoIncompleto(
        nombre="Incompleto",
        precio_base=100,
        stock_cantidad=10,
        unidad_venta=None,
        categoria_principal=Categoria("Test"),
        habilitado=True,
    )
except TypeError as e:
    print("OK:", e)


print("\n=== PRUEBA 3: ProductoSimple ===")
cat_g = Categoria("Golosinas")
u_unidad = UnidadMedida("Unidad", "u", "unidad")

p_simple = ProductoSimple("Alfajor", 500, 100, u_unidad, cat_g)
print("Precio simple (3 unidades):", p_simple.precio_final(3))


print("\n=== PRUEBA 4: ProductoPorPeso ===")
cat_f = Categoria("Fiambres")
u_kg = UnidadMedida("Kilogramo", "kg", "peso")

p_peso = ProductoPorPeso("Queso", 3200, 50, u_kg, cat_f)
print("Precio por peso (0.250 kg):", p_peso.precio_final(0.250))


print("\n=== PRUEBA 5: ProductoCombo ===")
combo = ProductoCombo(
    nombre="Desayuno",
    componentes=[p_simple, p_peso],
    descuento=0.10,
    precio_base=0,
    stock_cantidad=999,
    unidad_venta=None,
    categoria_principal=Categoria("Combos"),
)

print("Precio combo (1 unidad):", combo.precio_final(1))


print("\n=== PRUEBA 6: ProductoDestacado ===")
dest = ProductoDestacado(
    nombre="Yerba",
    precio_base=2500,
    stock_cantidad=200,
    unidad_venta=u_kg,
    categoria_principal=cat_g,
    orden_vidriera=1,
)

print("Precio destacado (2 unidades):", dest.precio_final(2))
print("Orden vidriera:", dest.orden_vidriera)


print("\n=== PRUEBA 7: Validación de cantidad en ProductoDestacado ===")
try:
    dest.precio_final(0)
except ValueError as e:
    print("OK:", e)


print("\n=== PRUEBA 8: Polimorfismo sin if/elif ===")
productos = [p_simple, p_peso, combo, dest]

for p in productos:
    print(f"{p.nombre}: {p.precio_final(1)}")


print("\n=== PRUEBA 9: Combo dentro de Combo ===")

# Categorías y unidades
cat_c = Categoria("Combos")
u_unidad = UnidadMedida("Unidad", "u", "unidad")
u_kg = UnidadMedida("Kilogramo", "kg", "peso")

# Productos base
p_simple2 = ProductoSimple("Galletitas", 300, 100, u_unidad, Categoria("Golosinas"))
p_peso2 = ProductoPorPeso("Jamón", 4500, 20, u_kg, Categoria("Fiambres"))

# Combo A (simple)
combo_A = ProductoCombo(
    nombre="Combo A",
    componentes=[p_simple2, p_peso2],
    descuento=0.20,     # 20% descuento
    precio_base=0,
    stock_cantidad=999,
    unidad_venta=None,
    categoria_principal=cat_c,
)

print("Precio Combo A (1 unidad):", combo_A.precio_final(1))

# Combo B (contiene Combo A + productos normales)
combo_B = ProductoCombo(
    nombre="Combo B",
    componentes=[combo_A, p_simple2, p_peso2],
    descuento=0.10,     # 10% descuento
    precio_base=0,
    stock_cantidad=999,
    unidad_venta=None,
    categoria_principal=cat_c,
)

print("Precio Combo B (1 unidad):", combo_B.precio_final(1))

# Combo C (combo dentro de combo dentro de combo)
combo_C = ProductoCombo(
    nombre="Combo C",
    componentes=[combo_B, combo_A],
    descuento=0.05,     # 5% descuento
    precio_base=0,
    stock_cantidad=999,
    unidad_venta=None,
    categoria_principal=cat_c,
)

print(f"Precio Combo C (1 unidad): {combo_C.precio_final(1):.2f}") # ! SIEMPRE REDONDEAR SALIDA DE COMBOS, SI NO PUEDE DAR .99999

print("\n=== PRUEBA 10: Exportación de productos ===")

print("Exportar ProductoSimple:", p_simple.exportar())
print("Exportar ProductoPorPeso:", p_peso.exportar())
print("Exportar ProductoCombo:", combo.exportar())
print("Exportar ProductoDestacado:", dest.exportar())


print("\n=== PRUEBA 11: Exportación de ficha externa ===")

ficha = FichaPuntoDeVenta("A12", "Pago en caja")
print("Exportar FichaPuntoDeVenta:", ficha.exportar())


print("\n=== PRUEBA 12: exportar_catalogo con productos y fichas mezclados ===")

items = [
    p_simple,
    p_peso,
    combo,
    dest,
    ficha,       # mezcla con clase externa
    combo_A,     # combos dentro de combos también exportan
]

from catalogo_old import exportar_catalogo  # donde definiste el Protocol y la función

resultado = exportar_catalogo(items)

for linea in resultado:
    print(linea)

print("\n=== PRUEBA 13: categoria duplicada ===")

def test_clasificacion_duplicada():
    print("\n=== TEST: Clasificación duplicada ===")

    # Categoría y unidad
    cat_golosinas = Categoria("Golosinas")
    u_unidad = UnidadMedida("Unidad", "u", "unidad")

    # Producto
    p = ProductoSimple("Alfajor", 500, 100, u_unidad, cat_golosinas)

    # Primera clasificación (válida)
    p.clasificar_en(Categoria("Promo"))  # categoría distinta

    # Segunda clasificación duplicada → debe fallar
    try:
        p.clasificar_en(cat_golosinas)  # misma categoría principal
        print("ERROR: No lanzó DomainError")
    except DomainError as e:
        print("OK:", e)

if __name__ == "__main__":
    test_clasificacion_duplicada()