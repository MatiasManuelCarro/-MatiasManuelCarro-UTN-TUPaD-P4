"""parte1_diagnostico.py — Versión corregida e idiomática en Python."""

from abc import ABC, abstractmethod


class Figura(ABC):
    def __init__(self, nombre: str, color: str) -> None:
        self.nombre = nombre
        self.color = color
        self._construida = True

    @abstractmethod
    def area(self) -> float:
        """Contrato formal: cada figura concreta debe calcular su propia área."""
        


class Lado:
    def __init__(self, longitud: float) -> None:
        self.longitud = longitud  # Pasa por el setter validando desde el inicio

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor


class Poligono(Figura):
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

    def agregar_observacion(self, texto: str) -> None:
        self._observaciones.append(texto)

    def lados(self) -> tuple[Lado, ...]:
        # Copia defensiva mediante tupla inmutable
        return tuple(self._lados)


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


if __name__ == "__main__":
    t = Triangulo("Triángulo", "rojo", [Lado(3), Lado(4), Lado(5)])
    c = Cuadrado("Cuadrado", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])
    print(f"Perímetro del triángulo: {t.perimetro()}")
    print(f"Perímetro del cuadrado: {c.perimetro()}")
    t.agregar_observacion("revisar el vértice A")
    print(f"Nombre: {t.nombre}")
