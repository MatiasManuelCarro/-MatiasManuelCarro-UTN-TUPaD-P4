
"""demo_property.py — Demostración de transición a @property.

Prueba que el código cliente no cambia su sintaxis al incorporar validación
mediante @property, a diferencia de los getters/setters estilo Java.
"""

# =====================================================================
# 1. ENFOQUE ANTES: Estilo Java Bean 
# =====================================================================


class LadoJavaismo:

    def __init__(self, longitud: float):
        self._longitud = longitud

    def getLongitud(self) -> float:
        return self._longitud

    def setLongitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser estrictamente positiva.")
        self._longitud = valor


# =====================================================================
# 2. ENFOQUE DESPUÉS: Idiomático con @property 
# =====================================================================


class LadoPythonico:

    def __init__(self, longitud: float):
        # Al asignar self.longitud pasa por el setter y valida desde el nacimiento
        self.longitud = longitud

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser estrictamente positiva.")
        self._longitud = valor


# =====================================================================
# 3. DEMOSTRACIÓN: Comparación del impacto en el Código Cliente
# =====================================================================


def probar_enfoque_java():
    print("--- Enfoque Antes (Estilo Java) ---\n")
    lado_java = LadoJavaismo(10.0)

    # El cliente está obligado a invocar métodos con paréntesis
    print(f"Lectura con getLongitud(): {lado_java.getLongitud()}")
    lado_java.setLongitud(25.5)
    print(f"Lectura tras setLongitud(25.5): {lado_java.getLongitud()}")

    # Además, el atributo interno queda expuesto si se accede por error
    lado_java._longitud = -999.0
    print(
        f"Demostracion: Se ignoro el setter asignando al atributo privado: {lado_java._longitud}\n"
    )


def probar_enfoque_python():
    print("\n--- Enfoque Python (@property) ---\n")

    # Supongamos que el cliente consumía atributos públicos normales:
    # lado = Lado(10.0)
    # total = lado.longitud + 5.0
    # lado.longitud = 25.5

    # Al migrar a @property, las líneas del cliente son exactamente las mismas:
    lado = LadoPythonico(10.0)

    # 1. Lectura directa (sintaxis de atributo sin paréntesis)
    print(f"Lectura directa (lado.longitud): {lado.longitud}")

    # 2. Asignación directa (sintaxis de atributo)
    lado.longitud = 25.5
    print(f"Lectura tras reasignación (lado.longitud = 25.5): {lado.longitud}")

    # 3. Operaciones matemáticas limpias
    perimetro_estimado = lado.longitud * 4
    print(f"Cálculo directo (lado.longitud * 4): {perimetro_estimado}")

    # 4. Verificación de la invariante: frena valores inválidos transparentemente
    print("Intentando asignar valor negativo (lado.longitud = -10.0)...")
    try:
        lado.longitud = -10.0
    except ValueError as error:
        print(f"Excepción capturada con éxito: {error}")

    print(
        f"El valor se mantuvo protegido en su último estado válido: {lado.longitud}"
    )


if __name__ == "__main__":
    probar_enfoque_java()
    probar_enfoque_python()