#parte1_diagnostico.py — Versión corregida e idiomática en Python."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Figura(ABC):
    def __init__(self, nombre: str, color: str) -> None:
        self.nombre = nombre
        self.color = color
        self._construida = True

    @abstractmethod
    def area(self) -> float:
        """Contrato formal: cada figura concreta debe calcular su propia área."""
        

@dataclass(frozen=True)
class Etiqueta:
    texto: str

class Lado:
    def __init__(
        self, longitud: float, etiqueta: Etiqueta | None = None
    ) -> None:
        self.longitud = longitud  # Setter con validación
        self.etiqueta: Etiqueta | None = etiqueta  # Asociación opcional 0..1

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor
    
    def __repr__(self) -> str:
        tag = f", etiqueta='{self.etiqueta.texto}'" if self.etiqueta else ""
        return f"Lado({self.longitud}{tag})"
    


class Poligono(Figura, ABC):
    def __init__(
        self,
        nombre: str,
        color: str,
        lados: list[Lado] | None = None,
        observaciones: list[str] | None = None,
    ) -> None:
        super().__init__(nombre, color)
        # Evitamos default mutable y aliasing creando copias defensivas
        self._lados = list(lados) if lados is not None else []
        self._observaciones = list(observaciones) if observaciones is not None else []

    @abstractmethod
    def lados_esperados(self) -> int:
        pass

    def perimetro(self) -> float:
        # Suma idiomática y pythónica usando generadores
        return sum(l.longitud for l in self._lados)

    def area(self) -> float:
        return 0.0
    
    def observaciones(self) -> tuple[str, ...]:
        # Copia defensiva mediante tupla inmutable
        return tuple(self._observaciones)

    def agregar_observacion(self, texto: str) -> None:
        self._observaciones.append(texto)

    def lados(self) -> tuple[Lado, ...]:
        # Copia defensiva mediante tupla inmutable
        return tuple(self._lados)
    
    def es_regular(self) -> bool:
        if not self._lados:
            return False
        primera_longitud = self._lados[0].longitud
        return all(lado.longitud == primera_longitud for lado in self._lados)


class Triangulo(Poligono):
    def __init__(
        self,
        nombre: str = "triángulo",
        color: str = "negro",
        lados: list[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 3
    
    @classmethod
    def regular(
        cls, nombre: str, color: str, longitud_lado: float
    ) -> "Triangulo":
        """Fabrica un triángulo regular (equilátero) de forma semántica."""
        return cls(nombre, color, [Lado(longitud_lado) for _ in range(3)])


class Cuadrado(Poligono):
    def __init__(
        self,
        nombre: str = "cuadrado",
        color: str = "negro",
        lados: list[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 4
    
    @classmethod
    def regular(
        cls, nombre: str, color: str, longitud_lado: float
    ) -> "Cuadrado":
        #Fabrica un cuadrado regular de forma semántica.
        return cls(nombre, color, [Lado(longitud_lado) for _ in range(4)])


class Pentagono(Poligono):

    def __init__(
        self,
        nombre: str = "pentágono",
        color: str = "negro",
        lados: list[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 5

    @classmethod
    def regular(
        cls, nombre: str, color: str, longitud_lado: float
    ) -> "Pentagono":
        return cls(nombre, color, [Lado(longitud_lado) for _ in range(5)])


class Hexagono(Poligono):

    def __init__(
        self,
        nombre: str = "hexágono",
        color: str = "negro",
        lados: list[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 6

    @classmethod
    def regular(
        cls, nombre: str, color: str, longitud_lado: float
    ) -> "Hexagono":
        return cls(nombre, color, [Lado(longitud_lado) for _ in range(6)])

class Taller:

    def __init__(self, poligonos: list[Poligono] | None = None) -> None:
        # Agregación: almacena referencias a polígonos creados externamente
        # Copia defensiva en la entrada
        self._inventario: list[Poligono] = (
            list(poligonos) if poligonos is not None else []
        )

    def recibir(self, poligono: Poligono) -> None:
        """Incorpora un polígono existente."""
        self._inventario.append(poligono)

    def restaurar_todos(self) -> None:
        """Restaura todos los polígonos del taller."""
        for p in self._inventario:
            p.agregar_observacion("Restaurado en taller")

    def inventario(self) -> tuple[Poligono, ...]:
        """Copia defensiva en la salida (multiplicidad *): tupla inmutable."""
        return tuple(self._inventario)


if __name__ == "__main__":
    # 1. Asociación (0..1): Lado — Etiqueta (con y sin etiqueta)
    e1 = Etiqueta("Base")
    lado_a = Lado(3.0, e1)
    lado_b = Lado(4.0)  # None por defecto

    print(f"Lado con etiqueta: {lado_a.etiqueta.texto}")
    print(f"Lado sin etiqueta: {lado_b.etiqueta}")

    # 2. Composición (3..*): Poligono — Lado
    triangulo = Triangulo("T1", "Rojo", [lado_a, lado_b, Lado(5.0)])
    cuadrado = Cuadrado("C1", "Azul", [Lado(2.0), Lado(2.0), Lado(2.0), Lado(2.0)])

    print(f"Perímetro T1: {triangulo.perimetro()}")
    print(f"Lados devueltos como tupla inmutable: {type(triangulo.lados())}")

    # 3. Agregación (0..*): Taller — Poligono (recibe figuras ya creadas)
    taller = Taller([triangulo])  # entra uno
    taller.recibir(cuadrado)  # entra otro
    taller.restaurar_todos()

    print(f"Figuras en taller: {len(taller.inventario())}")
    print(f"Observaciones del triángulo: {triangulo.observaciones()}")
    
    # 4. Nuevas subclases: Pentagono y Hexagono vía constructores regulares
    print("\nPruebas parte 3")
    penta = Pentagono.regular("Penta1", "Verde", 3.0)
    hexa = Hexagono.regular("Hexa1", "Amarillo", 2.5)

    print(
        f"{penta.nombre}: lados={len(penta.lados())}, perímetro={penta.perimetro()}, es_regular={penta.es_regular()}"
    )
    print(
        f"{hexa.nombre}: lados={len(hexa.lados())}, perímetro={hexa.perimetro()}, es_regular={hexa.es_regular()}"
    )

    # Figura no regular para comparar
    tri_escaleno = Triangulo(
        "Escaleno", "Gris", [Lado(3.0), Lado(4.0), Lado(5.0)]
    )
    print(
        f"{tri_escaleno.nombre}: es_regular={tri_escaleno.es_regular()}\n"
    )

    print("=== DEMOSTRACIÓN DE FALLA TEMPRANA  ===")

    # Falla Temprana A: Instanciar Poligono directamente o subclase incompleta sin lados_esperados()
    class PoligonoIncompleto(Poligono):
        pass  # No implementa lados_esperados()

    try:
        figura_rota = PoligonoIncompleto("Incompleto", "Negro")
    except TypeError as e:
        print(f"Falla temprana exitosa (TypeError al construir): {e}")

    try:
        poligono_directo = Poligono("Abstracto", "Blanco")
    except TypeError as e:
        print(f"Falla temprana directa (TypeError al construir ABC): {e}")

    # Falla Temprana B: Cantidad incorrecta de lados viola contrato de figura
    try:
        # Pentagono espera 5 lados, le pasamos solo 3
        penta_invalido = Pentagono(
            "PentaInvalido", "Rojo", [Lado(2.0), Lado(2.0), Lado(2.0)]
        )
    except ValueError as e:
        print(f"Falla temprana exitosa (ValueError por cantidad de lados): {e}")
