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

print("\nDEMO — Food Store")

# ============================================================
# * Falla temprana producto abstracto
print("\n....................................................")
print("\n=== Falla temprana: Producto abstracto ===\n")
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
    print("Falla temprana en creacion producto abstracto: ", e)

# ============================================================
# * Categorías y unidades
cat_snacks = Categoria("Snacks")
cat_bebidas = Categoria("Bebidas")
cat_fiambres = Categoria("Fiambres")
cat_infusiones = Categoria("Infusiones")
cat_combos = Categoria("Combos")

u_unidad = UnidadMedida("Unidad", "u", "unidad")
u_kg = UnidadMedida("Kilogramo", "kg", "peso")
u_litro = UnidadMedida("Litro", "l", "volumen")

# ============================================================
# * Productos 
print("\n....................................................")
print("\n=== Creación de productos ===\n")

productos: list[Producto] = []

# ProductoSimple
alfajor = ProductoSimple("Alfajor", 2000, 100, u_unidad, cat_snacks)
productos.append(alfajor)

galletitas = ProductoSimple("Galletitas", 1500, 80, u_unidad, cat_snacks)
productos.append(galletitas)

papas = ProductoSimple("Papas Fritas", 2500, 120, u_unidad, cat_snacks)
productos.append(papas)

jugo = ProductoSimple("Jugo", 1200, 200, u_litro, cat_bebidas)
productos.append(jugo)

coca_cola = ProductoSimple("Coca-Cola", 4000, 150, u_litro, cat_bebidas)
productos.append(coca_cola)

# ProductoPorPeso
queso = ProductoPorPeso("Queso", 3200, 50, u_kg, cat_fiambres)
productos.append(queso)

jamon = ProductoPorPeso("Jamón", 2800, 40, u_kg, cat_fiambres)
productos.append(jamon)

# ProductoDestacado
yerba = ProductoSimple("Yerba", 3000, 200, u_kg, cat_infusiones)
productos.append(yerba)

destacado = ProductoDestacado(yerba, orden_vidriera=1)

print("\nProductos y sus categorías: \n")
for prod in productos:
    cats = ", ".join(c.nombre for c in prod.categorias)
    print(f"{prod.nombre} | Categorías: {cats}")

# ============================================================
# * Mostrar producto destacado

print("\n....................................................")
print("\n=== Producto Destacado ===\n")

print(f"Nombre: {destacado.producto.nombre}")
print(f"Categoría: {destacado.producto.categoria_principal.nombre}")
print(f"Orden de vidriera: {destacado.orden_vidriera}")
print(f"Precio publicado: {destacado.producto.precio_publicado}")

# ============================================================
# * Combos 
print("\n....................................................")
print("\n=== Combos: ===\n")

combos: list[ProductoCombo] = []

combo_desayuno = ProductoCombo(
    nombre="Combo Desayuno",
    componentes=[alfajor, jugo],
    descuento=0.10,
    unidad_venta=None,
    categoria_principal=cat_combos,
)
combos.append(combo_desayuno)

combo_merienda = ProductoCombo(
    nombre="Combo Merienda",
    componentes=[galletitas, jugo],
    descuento=0.15,
    unidad_venta=None,
    categoria_principal=cat_combos,
)
combos.append(combo_merienda)

combo_picada = ProductoCombo(
    nombre="Combo Picada",
    componentes=[queso, jamon, papas],
    descuento=0.15,
    unidad_venta=None,
    categoria_principal=cat_combos,
)
combos.append(combo_picada)

combo_picada_bebida = ProductoCombo(
    nombre="Combo Picada Bebida",
    componentes=[queso, jamon, papas, coca_cola],
    descuento=0.20,
    unidad_venta=None,
    categoria_principal=cat_combos,
)
combos.append(combo_picada_bebida)

for combo in combos:
    comps = ", ".join(p.nombre for p in combo.componentes)
    print(f"{combo.nombre} | Componentes: {comps} | Descuento: {combo._descuento * 100:.0f}%")

# ============================================================
# * Cálculo de precios finales
print("\n....................................................")
print("\n=== Cálculo de precios finales ===\n")
print("Alfajor x3:", alfajor.precio_final(3))
print("Queso 0.250kg:", queso.precio_final(0.250))
print("Combo Desayuno x1:", combo_desayuno.precio_final(1))
print("Combo Picada x2:", combo_picada.precio_final(2))

# ============================================================
# * Ficha externa
print("\n....................................................")
print("\n=== Ficha externa ===\n")
ficha = FichaPuntoDeVenta("A12", "Pago en caja")
print("Ficha externa exportada:", ficha.exportar())

# ============================================================
# * Exportación completa del catálogo
print("\n....................................................")
print("\n=== Exportación completa del catálogo ===\n")

catalogo: list = []

# Agregando productos a la lista del catalogo
catalogo.extend(productos)

# Agregamos combos
catalogo.extend(combos)

# Agregando destacado y ficha
catalogo.append(destacado)
catalogo.append(ficha)

exportados = exportar_catalogo(catalogo)

for linea in exportados:
    print(linea)

print("\n=== DEMO COMPLETA ===")
