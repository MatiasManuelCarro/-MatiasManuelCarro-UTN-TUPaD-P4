from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class Exportable(Protocol):

    def exportar(self) -> str:
        """Contrato estructural: exige un método exportar sin requerir herencia."""
        ...

@dataclass(frozen=True)
class Etiqueta:
    texto: str

def exportar_todo(items: list[Exportable]) -> list[str]:
    """Procesa cualquier objeto que cumpla con el protocolo Exportable.

    Acepta tanto figuras del dominio propio como clases de librerías externas
    (PlanoCAD).
    """
    return [item.exportar() for item in items]


class Figura(ABC):
    def __init__(self, nombre: str, color: str) -> None:
        self.nombre = nombre
        self.color = color
        self._construida = True

    @abstractmethod
    def area(self) -> float:
        """Contrato formal: cada figura concreta debe calcular su propia área."""
        


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
    
    def exportar(self) -> str:
        """Satisface estructuralmente el protocolo Exportable."""
        return (
            f"[{self.__class__.__name__.upper()}] nombre='{self.nombre}', "
            f"color='{self.color}', lados={len(self._lados)}, perimetro={self.perimetro():.2f}"
        )


# =====================================================================
# Subclases Concretas
# =====================================================================

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
        
# =====================================================================
# Taller
# =====================================================================

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


