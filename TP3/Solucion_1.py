import math
from dataclasses import dataclass, field
from typing import List 

#TODO citar porque uso list
#TODO explicar el uso de field

# Catálogo global explícito
catalogo = []

# -------------------------
# Figura base
# -------------------------

@dataclass
class Figura:
    nombre: str
    color: str

    def area(self) -> float:
        return 0.0

# -------------------------
# Lado con validación
# -------------------------

class Lado:
    def __init__(self, longitud: float):
        self.longitud = longitud   # pasa por el setter

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor

# -------------------------
# Poligono genérico
# -------------------------

@dataclass
class Poligono(Figura):
    lados: list = field(default_factory=list)
    observaciones: list = field(default_factory=list)

    def __post_init__(self):
        catalogo.append(self)

    def lados_esperados(self) -> int:
        return 0

    def perimetro(self) -> float:
        return sum(l.longitud for l in self.lados)

    def area(self) -> str:
        return "area sin calcular"

    def agregar_observacion(self, texto: str):
        self.observaciones.append(texto)

    @property
    def lados_detalle(self):
        return list(self.lados)

# -------------------------
# Triangulo
# -------------------------

@dataclass
class Triangulo(Poligono):
    nombre: str = "triángulo"
    color: str = "negro"
    lados: list = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        if len(self.lados) != 3:
            raise ValueError("Un triángulo debe tener exactamente 3 lados")

    @classmethod
    def desde_lados(cls, lados):
        if len(lados) != 3:
            raise ValueError("La lista debe tener 3 lados")
        return cls(lados=lados)

    def lados_esperados(self) -> int:
        return 3

# -------------------------
# Cuadrado
# -------------------------

@dataclass
class Cuadrado(Poligono):
    nombre: str = "cuadrado"
    color: str = "negro"
    lados: list = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        if len(self.lados) != 4:
            raise ValueError("Un cuadrado debe tener exactamente 4 lados")

    @classmethod
    def desde_lados(cls, lados):
        if len(lados) != 4:
            raise ValueError("La lista debe tener 4 lados")
        return cls(lados=lados)

    def lados_esperados(self) -> int:
        return 4

# -------------------------
# Main
# -------------------------

if __name__ == "__main__":
    activo = True

    if activo:
        t = Triangulo(
            nombre="Triángulo",
            color="rojo",
            lados=[Lado(3), Lado(4), Lado(5)]
        )

        c = Cuadrado(
            nombre="Cuadrado",
            color="azul",
            lados=[Lado(2), Lado(2), Lado(2), Lado(2)]
        )

        print(f"Perímetro del triángulo: {t.perimetro()}")
        print(f"Perímetro del cuadrado: {c.perimetro()}")

        t.agregar_observacion("revisar el vértice A")

        print(f"Figuras en el catálogo: {len(catalogo)}")
        print(f"Nombre: {t.nombre}")