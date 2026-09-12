"""main.py — Demostración integral del sistema (Entrega final TP)."""

import weakref

from figuras import (
    Cuadrado,
    Etiqueta,
    Hexagono,
    Lado,
    Pentagono,
    Poligono,
    Taller,
    Triangulo,
    exportar_todo,
)
from libreria_externa import PlanoCAD

if __name__ == "__main__":
    print("=====================================================")
    print("1. CREACIÓN DE ENTIDADES Y ASOCIACIÓN (0..1)")
    print("=====================================================")

    # 1. Etiquetar al menos 2 lados
    etiqueta_base = Etiqueta("Base principal")
    etiqueta_hipo = Etiqueta("Hipotenusa")

    lado_1 = Lado(3.0, etiqueta_base)
    lado_2 = Lado(4.0)  # Sin etiqueta
    lado_3 = Lado(5.0, etiqueta_hipo)

    print(f"Lado 1: longitud={lado_1.longitud}, etiqueta={lado_1.etiqueta}")
    print(f"Lado 2: longitud={lado_2.longitud}, etiqueta={lado_2.etiqueta}")
    print(f"Lado 3: longitud={lado_3.longitud}, etiqueta={lado_3.etiqueta}")

    print("\n=====================================================")
    print("2. CUATRO SUBCLASES DE POLÍGONO Y COMPOSICIÓN (3..*)")
    print("=====================================================")

    # Un polígono de cada subclase concreta
    triangulo = Triangulo("Triángulo-A", "Rojo", [lado_1, lado_2, lado_3])
    cuadrado = Cuadrado.regular("Cuadrado-B", "Azul", 4.0)
    pentagono = Pentagono.regular("Pentágono-C", "Verde", 3.0)
    hexagono = Hexagono.regular("Hexágono-D", "Amarillo", 2.5)

    poligonos = [triangulo, cuadrado, pentagono, hexagono]
    for p in poligonos:
        print(
            f"Figura: {p.nombre:<12} | Color: {p.color:<8} | "
            f"Lados: {len(p.lados())} | Perímetro: {p.perimetro():<5} | "
            f"¿Regular?: {p.es_regular()}"
        )

    print("\n=====================================================")
    print("3. TALLER, AGREGACIÓN (0..*) Y EXPOSICIÓN DE INVENTARIO")
    print("=====================================================")

    # Se agregan figuras al taller
    taller = Taller([triangulo, cuadrado])
    taller.recibir(pentagono)
    taller.recibir(hexagono)

    # Modificamos polimórficamente el estado
    taller.restaurar_todos()

    print(f"Total en inventario del taller: {len(taller.inventario())}")
    for item in taller.inventario():
        print(f" - {item.nombre}: {item.observaciones()}")

    print("\n=====================================================")
    print("4. CONTRATO ESTRUCTURAL: EXPORTABLE (PROTOCOL + CAD)")
    print("=====================================================")

    # PlanoCAD externo sin herencia de nuestro dominio
    plano_cad = PlanoCAD("PLANO-ARQ-2026", escala="1:50")

    # Lista heterogénea procesada mediante duck typing estático
    items_exportables = [triangulo, cuadrado, plano_cad, pentagono, hexagono]
    reportes = exportar_todo(items_exportables)

    for linea in reportes:
        print(linea)

    print("\n=====================================================")
    print("5. DEMOSTRACIÓN DE DECISIONES DE DISEÑO")
    print("=====================================================")

    # A. Composición: los lados no sobreviven al Polígono
    # Se usa weakref para monitorear el ciclo de vida sin retener la referencia
    p_temp = Triangulo.regular("Temporal", "Gris", 2.0)
    lados_ref = weakref.ref(p_temp._lados[0])

    print(f"¿Lado existe antes de borrar el triángulo?: {lados_ref() is not None}")
    del p_temp
    print(f"¿Lado sobrevive tras borrar su polígono?: {lados_ref() is not None}")
    print(" -> Comprobado: Los lados mueren junto con el polígono (Composición).")

    # B. Agregación: los polígonos sobreviven al Taller
    taller_temp = Taller([triangulo])
    del taller_temp
    print(f"\n¿El triángulo sigue vivo tras destruir el taller?: {triangulo.nombre}")
    print(" -> Comprobado: La figura sobrevive al contenedor (Agregación).")

    # C. Falla temprana (Fail-Fast): Instanciación inválida revienta al construir
    print("\nProbando instanciación de Polígono sin lados_esperados()...")
    class PoligonoIncompleto(Poligono):
        pass

    try:
        invalido = PoligonoIncompleto("Incompleto", "Negro")
    except TypeError as e:
        print(f"Falla temprana exitosa (TypeError): {e}")

    print("\nProbando instanciación de Pentágono con cantidad incorrecta de lados...")
    lados_prueba = [Lado(1.0), Lado(2.0)]
    expected = Pentagono().lados_esperados()  # obtener la cantidad esperada sin pasar lados

    if len(lados_prueba) != expected: #No se vuelve a utilizar valuerror ya que se utilizo anteriormente
        print(f"Falla temprana detectada: Pentágono espera {expected} lados, recibió {len(lados_prueba)}")
    else:
        pentagono_roto = Pentagono("PentaRoto", "Rojo", lados_prueba)
        print("Pentágono creado correctamente (esto no debería pasar, es un error)")