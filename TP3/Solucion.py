import math
from dataclasses import dataclass, field
from typing import List #TODO citar porque uso list
#TODO explicar el uso de field

@dataclass
class Figura:
    nombre: str
    color: str

    def area(self) -> float:
        return 0.0

class Lado:
    def __init__(self, longitud: float):
        self.longitud = longitud

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

@dataclass
class Poligono:
    nombre: str
    color: str
    lados: List[int] = field(default_factory=list)
    observaciones: List[str] = field(default_factory=list)