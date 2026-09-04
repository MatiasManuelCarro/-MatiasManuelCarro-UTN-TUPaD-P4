"""demo_sintomas.py
Demostración de 2 síntomas observables producidos por Java-ismos
en parte1_diagnostico.py (antes de ser corregidos).
"""
import sys

# Importamos el módulo original con problemas
import parte1_diagnostico as diag


def demostrar_sintoma_default_mutable():
    print("=== SÍNTOMA 1: Argumento por defecto mutable (observaciones=[]) ===")
    p1 = diag.Poligono("Poligono 1", "Rojo")
    p2 = diag.Poligono("Poligono 2", "Azul")

    p1.agregar_observacion("Observación exclusiva de P1")

    print(f"\nObservaciones de p1: {p1._observaciones}")
    print(f"\nObservaciones de p2: {p2._observaciones}")
    
    # Comprobación de identidad de memoria:
    comparten_memoria = p1._observaciones is p2._observaciones
    print(f"\n¿p1 y p2 comparten la misma lista en memoria?: {comparten_memoria}")
    assert comparten_memoria, "\nDeberían compartir memoria en el código sin corregir"
    print("\-> SÍNTOMA CONFIRMADO: Mutar p1 alteró silenciosamente a p2.\n")


def demostrar_sintoma_fuga_encapsulamiento():
    print("=== SÍNTOMA 2: Fuga de encapsulamiento por falta de copia defensiva ===")
    lados_iniciales = [diag.Lado(3), diag.Lado(4), diag.Lado(5)]
    tri = diag.Triangulo("Triángulo", "Verde", lados_iniciales)

    print(f"Perímetro original: {tri.perimetro()}")
    
    # Un cliente externo obtiene los lados y los muta directamente:
    lados_expuestos = tri.getLados()
    lados_expuestos.clear()  # Vaciamos la lista desde afuera

    print(f"Perímetro luego de tri.getLados().clear(): {tri.perimetro()}")
    print(f"¿La lista interna quedó vacía?: {len(tri._lados) == 0}")
    assert len(tri._lados) == 0, "La lista interna debió haberse vaciado por aliasing"
    print("-> SÍNTOMA CONFIRMADO: El cliente destruyó el estado interno del objeto.\n")


if __name__ == "__main__":
    demostrar_sintoma_default_mutable()
    demostrar_sintoma_fuga_encapsulamiento()