# test_caos.py
# Ejecutar con: pytest -q test_caos.py

import math
import pytest

from catalogo import (
    Categoria,
    DomainError,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    UnidadMedida
)

# ! ESTOS ATAQUES DAN PASS PORQUE EL CODIGO ES VULNERABLE - TENER EN CUENTA PARA UN FUTURO 

# ---------------------------------------------------------
# ATAQUE 1: Envenenamiento con NaN (Not a Number)
# ---------------------------------------------------------
def test_ataque_nan_corrompe_calculos_silenciosamente():
    """
    VULNERABILIDAD: En Python, math.isnan(float('nan') < 0) evalúa a False.
    Por lo tanto, if precio_base < 0: ¡deja pasar el NaN!
    """
    c = Categoria("Caos")
    u = UnidadMedida("Kg", "kg", "masa")
    
    # ProductoPorPeso valida: if precio_base <= 0: raise ...
    # NaN no es <= 0, así que pasa la barrera de defensa.
    p = ProductoPorPeso("Manzanas Tóxicas", float('nan'), 100, u, c)
    
    # El precio final se corrompe y propaga NaN silenciosamente a todo el sistema.
    precio_a_cobrar = p.precio_final(5)
    
    # Esto pasará (lo cual demuestra que el dominio está roto)
    assert math.isnan(precio_a_cobrar)

# ---------------------------------------------------------
# ATAQUE 2: Recursión Infinita (Combos Circulares)
# ---------------------------------------------------------
def test_ataque_combo_recursivo_destruye_el_stack():
    """
    VULNERABILIDAD: Un ProductoCombo no verifica si se contiene a sí mismo
    (ya sea directa o indirectamente).
    """
    c = Categoria("Caos")
    u = UnidadMedida("Unidad", "u", "u")
    p1 = ProductoSimple("A", 100, 10, u, c)
    
    combo1 = ProductoCombo("Combo 1", [p1, p1], 0.1, u, c)
    combo2 = ProductoCombo("Combo 2", [p1, combo1], 0.1, u, c)
    
    # Simulamos un error de base de datos o un hack a la lista interna:
    # Combo 1 ahora contiene al Combo 2, que contiene al Combo 1...
    combo1._componentes[1] = combo2 
    
    # Al pedir el precio, entra en un loop infinito y la aplicación crashea con RecursionError
    # (No lanza DomainError, rompe el intérprete)
    with pytest.raises(RecursionError):
        _ = combo1.precio_base

# ---------------------------------------------------------
# ATAQUE 3: Evasión de validación de strings (Unicode Invisible)
# ---------------------------------------------------------
def test_ataque_nombres_invisibles():
    """
    VULNERABILIDAD: El método .strip() limpia espacios normales, 
    pero ignora los caracteres de espacio de ancho cero (Zero-Width Space).
    """
    c = Categoria("Caos")
    u = UnidadMedida("Unidad", "u", "u")
    
    invisible_name = "\u200B\u200B" # Caracteres Unicode invisibles
    
    # La validación 'if not nombre.strip():' no los detecta.
    p = ProductoSimple(invisible_name, 100, 10, u, c)
    
    # El producto se creó exitosamente sin nombre visible
    assert p.nombre == invisible_name
    assert p.exportar().startswith("PROD|\u200B\u200B|100")

# ---------------------------------------------------------
# ATAQUE 4: Booleanos infiltrados como Enteros
# ---------------------------------------------------------
def test_ataque_bool_como_entero():
    """
    VULNERABILIDAD: En Python, bool hereda de int. True == 1 y False == 0.
    """
    c = Categoria("Caos")
    u = UnidadMedida("Unidad", "u", "u")
    
    # ProductoSimple valida: if precio_base < 1 or precio_base != int(precio_base):
    # True < 1 es False. True != int(True) es 1 != 1 (False).
    # ¡Pasa la validación siendo un booleano!
    p = ProductoSimple("HackBool", True, 10, u, c)
    
    assert p.precio_base is True
    # Matemáticamente funciona, pero conceptualmente el dominio fue engañado
    assert p.precio_final(True) == 1 

# ---------------------------------------------------------
# ATAQUE 5: Pérdida de Precisión Flotante en Stock
# ---------------------------------------------------------
def test_ataque_precision_flotante_stock():
    """
    VULNERABILIDAD: Sumas de floats en base 2.
    """
    c = Categoria("Caos")
    u = UnidadMedida("Unidad", "u", "u")
    
    p = ProductoSimple("Stock Roto", 100, 0.1, u, c)
    
    p.ajustar_stock(0.2)
    # Internamente ahora es 0.30000000000000004
    
    # Descontamos 0.3 exactamente
    p.ajustar_stock(-0.3)
    
    # Debería ser 0 y estar NO disponible, pero queda un residuo microscópico
    # (0.00000000000000004) por lo que sigue activo en el catálogo.
    assert p.stock_cantidad > 0
    assert p.disponible is True
    
# ---------------------------------------------------------
# ESTO HACE QUE CORRA AL DARLE PLAY
# ---------------------------------------------------------
if __name__ == "__main__":
    pytest.main(["-v", __file__])