"""demo_sintomas.py — Demostración de síntomas antes de corregir los java-ismos.

Muestra dos fallas reproducibles del código original de parte1_diagnostico.py:
Argumentos por defecto mutables (Java-ismo #4).
Falta de copia defensiva / Aliasing accidental (Java-ismo #6).
"""


class PoligonoOriginal:
    # Simula el constructor original con defaults mutables y asignación directa sin copia
    #El linter informa: Do not use mutable data structures for argument 
    def __init__(self, lados=[], observaciones=[]):
        self._lados = lados  # Aliasing: guarda la referencia directa
        self._observaciones = observaciones  # Default mutable


def demostrar_sintoma_1_default_mutable():
    print("--- SÍNTOMA 1: Argumento por defecto mutable (observaciones=[]) ---")

    # Creamos dos instancias usando el valor por defecto
    p1 = PoligonoOriginal()
    p2 = PoligonoOriginal()

    # Agregamos una observación únicamente al primer polígono
    p1._observaciones.append("Revisar vértice A")

    # Verificación de identidad en memoria
    mismo_objeto = p1._observaciones is p2._observaciones

    print(f"¿p1._observaciones es el mismo objeto que p2._observaciones?: {mismo_objeto}")
    print(f"Observaciones de p1: {p1._observaciones}")
    print(f"Observaciones de p2 (sin haberle agregado nada): {p2._observaciones}")

    print(
        "Fallo observable: p2 quedó contaminado con los datos de p1 "
        "porque ambos comparten la misma lista creada en tiempo de definición."
    )


def demostrar_sintoma_2_aliasing_sin_copia_defensiva():
    print("\n--- SÍNTOMA 2: Violación de encapsulamiento por falta de copia defensiva ---")

    lista_externa = ["LadoA", "LadoB", "LadoC"]

    # Instanciamos el polígono pasándole la lista externa
    p = PoligonoOriginal(lados=lista_externa)

    print(f"Lados internos de p al iniciar: {p._lados}")

    # Un actor externo modifica su propia lista después de haber creado el objeto
    lista_externa.clear()

    print(f"Lados internos de p tras vaciar la lista externa: {p._lados}")

    print(
        "Fallo observable: el estado interno de p fue corrompido desde afuera sin pasar "
        "por ningún método del polígono, porque se guardó el alias en vez de una copia."
    )


if __name__ == "__main__":
    demostrar_sintoma_1_default_mutable()
    demostrar_sintoma_2_aliasing_sin_copia_defensiva()

