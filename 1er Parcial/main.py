from catalogo import (
    Categoria,
    Producto,
    ProductoCombo,
    ProductoDestacado,
    ProductoPorPeso,
    ProductoSimple,
    UnidadMedida,
    exportar_catalogo,
)
from libreria_externa import FichaPuntoDeVenta

print("\n=== DEMO EJECUTABLE — Requerimiento 5 ===")

# ============================================================
# 1. Falla temprana: Producto es abstracto → no se puede instanciar
# ============================================================
print("\n=== Falla temprana: Producto abstracto ===")
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

# ============================================================
# 2. Categorías y unidades (agregación)
# ============================================================
cat_golosinas = Categoria("Golosinas")
cat_fiambres = Categoria("Fiambres")
cat_bebidas = Categoria("Bebidas")
cat_combos = Categoria("Combos")

u_unidad = UnidadMedida("Unidad", "u", "unidad")
u_kg = UnidadMedida("Kilogramo", "kg", "peso")
u_litro = UnidadMedida("Litro", "l", "volumen")

# ============================================================
# 3. Productos concretos (al menos 4, sin contar componentes de combos)
# ============================================================

print("\n=== Creación de productos concretos ===")

p_simple = ProductoSimple("Alfajor", 500, 100, u_unidad, cat_golosinas)
print("ProductoSimple creado:", p_simple.nombre)

p_peso = ProductoPorPeso("Queso", 3200, 50, u_kg, cat_fiambres)
print("ProductoPorPeso creado:", p_peso.nombre)

p_simple2 = ProductoSimple("Galletitas", 300, 80, u_unidad, cat_golosinas)
print("ProductoSimple creado:", p_simple2.nombre)

p_bebida = ProductoSimple("Jugo", 900, 200, u_litro, cat_bebidas)
print("ProductoSimple creado:", p_bebida.nombre)

# ============================================================
# 4. Composición: ProductoCombo contiene productos
# ============================================================

print("\n=== ProductoCombo (composición) ===")

combo_desayuno = ProductoCombo(
    nombre="Combo Desayuno",
    componentes=[p_simple, p_peso],  # los componentes sobreviven → agregación
    descuento=0.10,
    unidad_venta=None,
    categoria_principal=cat_combos,
)

print("Combo creado:", combo_desayuno.nombre)

# ============================================================
# 5. Agregación: los componentes sobreviven y pueden reutilizarse
# ============================================================

print("\n=== Agregación: componentes reutilizados ===")

combo_snack = ProductoCombo(
    nombre="Combo Snack",
    componentes=[p_simple2, p_bebida],  # reutilización → agregación
    descuento=0.15,
    unidad_venta=None,
    categoria_principal=cat_combos,
)

print("Combo creado:", combo_snack.nombre)


# ============================================================
# 6. ProductoDestacado (Rediseñado con Composición)
# ============================================================
print("\n=== ProductoDestacado ===")

# Tomamos un producto existente y lo destacamos
dest = ProductoDestacado(producto=p_peso, orden_vidriera=1)

print("ProductoDestacado creado envolviendo a:", dest.producto.nombre)

print("Queso Destacado x2:", dest.producto.precio_final(2))

# ============================================================
# 7. Cálculo de precios finales
# ============================================================

print("\n=== Cálculo de precios finales ===")
print("Alfajor x3:", p_simple.precio_final(3))
print("Queso 0.250kg:", p_peso.precio_final(0.250))
print("Combo Desayuno x1:", combo_desayuno.precio_final(1))
print("Combo Snack x1:", combo_snack.precio_final(1))
print("Yerba x2:", dest.producto.precio_final(2))

# ============================================================
# 8. Ficha externa (librería externa)
# ============================================================

print("\n=== Ficha externa ===")
ficha = FichaPuntoDeVenta("A12", "Pago en caja")
print("Ficha externa exportada:", ficha.exportar())

# ============================================================
# 9. Exportación completa del catálogo (Protocol)
# ============================================================

print("\n=== Exportación completa del catálogo ===")

catalogo = [
    p_simple,
    p_peso,
    p_simple2,
    p_bebida,
    combo_desayuno,
    combo_snack,
    dest,
    ficha,  # mezcla con clase externa
]

exportados = exportar_catalogo(catalogo)

for linea in exportados:
    print(linea)

print("\n=== DEMO COMPLETA ===")
