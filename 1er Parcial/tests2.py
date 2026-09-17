import unittest
from dataclasses import FrozenInstanceError
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

class TestCatalogoFoodStore(unittest.TestCase):
    def setUp(self):
        # Objetos base válidos para usar en los tests
        self.u_kg = UnidadMedida("Kilogramo", "kg", "masa")
        self.u_un = UnidadMedida("Unidad", "u", "unidad")
        self.cat_ppal = Categoria("General")
        self.cat_extra = Categoria("Extra")

    # ==========================================
    # 1. ROMPIENDO LAS CLASES BASE
    # ==========================================
    def test_unidad_medida_inmutable(self):
        # Intento de modificar una dataclass frozen
        with self.assertRaises(FrozenInstanceError):
            self.u_kg.simbolo = "g"

    def test_categoria_invalida(self):
        # Nombres vacíos o puros espacios
        with self.assertRaises(DomainError):
            Categoria("")
        with self.assertRaises(DomainError):
            Categoria("   ")

    def test_producto_abstracto(self):
        # Falla temprana: No se puede instanciar Producto
        with self.assertRaises(TypeError):
            Producto("Test", 100, 10, self.u_un, self.cat_ppal)

    # ==========================================
    # 2. ROMPIENDO PRODUCTO SIMPLE
    # ==========================================
    def test_producto_simple_atributos_invalidos(self):
        # Nombre vacío
        with self.assertRaises(DomainError):
            ProductoSimple(" ", 100, 10, self.u_un, self.cat_ppal)
        # Precio base negativo
        with self.assertRaises(DomainError):
            ProductoSimple("Alfajor", -10, 10, self.u_un, self.cat_ppal)
        # Stock negativo
        with self.assertRaises(DomainError):
            ProductoSimple("Alfajor", 100, -5, self.u_un, self.cat_ppal)
        # Precio base float (ProductoSimple exige entero)
        with self.assertRaises(DomainError):
            ProductoSimple("Alfajor", 100.5, 10, self.u_un, self.cat_ppal)
        # Precio base cero (ProductoSimple exige >= 1)
        with self.assertRaises(DomainError):
            ProductoSimple("Alfajor", 0, 10, self.u_un, self.cat_ppal)

    def test_producto_simple_calculo_invalido(self):
        p = ProductoSimple("Alfajor", 100, 10, self.u_un, self.cat_ppal)
        # Cantidad negativa
        with self.assertRaises(DomainError):
            p.precio_final(-2)
        # Cantidad float no entera
        with self.assertRaises(DomainError):
            p.precio_final(2.5)
        # Cantidad cero
        with self.assertRaises(DomainError):
            p.precio_final(0)

    # ==========================================
    # 3. ROMPIENDO PRODUCTO POR PESO
    # ==========================================
    def test_producto_peso_atributos_invalidos(self):
        # Precio base cero o negativo (exige > 0)
        with self.assertRaises(DomainError):
            ProductoPorPeso("Queso", 0, 10, self.u_kg, self.cat_ppal)

    def test_producto_peso_calculo_invalido(self):
        p = ProductoPorPeso("Queso", 1000, 10, self.u_kg, self.cat_ppal)
        # Cantidad negativa
        with self.assertRaises(DomainError):
            p.precio_final(-0.5)
        # Cantidad cero
        with self.assertRaises(DomainError):
            p.precio_final(0)
        
        # Prueba de redondeo exitoso
        self.assertEqual(p.precio_final(0.333), 333.0)

    # ==========================================
    # 4. ROMPIENDO LAS CLASIFICACIONES (VÍNCULOS)
    # ==========================================
    def test_clasificacion_duplicada(self):
        p = ProductoSimple("Alfajor", 100, 10, self.u_un, self.cat_ppal)
        # Clasificar de nuevo en la misma categoría
        with self.assertRaises(DomainError):
            p.clasificar_en(self.cat_ppal)

    def test_encapsulamiento_colecciones(self):
        p = ProductoSimple("Alfajor", 100, 10, self.u_un, self.cat_ppal)
        # Intentar meter basura en la tupla devuelta no debería afectar al producto
        tupla_categorias = p.categorias
        with self.assertRaises(AttributeError):
            tupla_categorias.append("Basura") # Las tuplas no tienen append

    # ==========================================
    # 5. ROMPIENDO PRODUCTO COMBO
    # ==========================================
    def test_combo_atributos_invalidos(self):
        p1 = ProductoSimple("A", 100, 10, self.u_un, self.cat_ppal)
        p2 = ProductoPorPeso("B", 1000, 10, self.u_kg, self.cat_ppal)
        
        # Menos de 2 componentes
        with self.assertRaises(DomainError):
            ProductoCombo("Combo", [p1], 0.1, None, self.cat_ppal)
        
        # Componente que no es Producto (inyectando un string)
        with self.assertRaises(DomainError):
            ProductoCombo("Combo", [p1, "Infiltrado"], 0.1, None, self.cat_ppal)
            
        # Descuento fuera de rango [0, 1)
        with self.assertRaises(DomainError):
            ProductoCombo("Combo", [p1, p2], 1.5, None, self.cat_ppal)
        with self.assertRaises(DomainError):
            ProductoCombo("Combo", [p1, p2], -0.1, None, self.cat_ppal)

    def test_combo_disponibilidad_derivada(self):
        p1 = ProductoSimple("A", 100, 10, self.u_un, self.cat_ppal)
        p2 = ProductoSimple("B", 200, 10, self.u_un, self.cat_ppal)
        combo = ProductoCombo("Combo", [p1, p2], 0.1, None, self.cat_ppal)
        
        self.assertTrue(combo.disponible)
        
        # Si un componente se queda sin stock, el combo DEBE romperse (dar False)
        p1._stock_cantidad = 0 
        self.assertFalse(combo.disponible)

if __name__ == '__main__':
    unittest.main(verbosity=2)