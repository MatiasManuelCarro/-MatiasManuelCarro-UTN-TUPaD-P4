from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class DomainError(ValueError): # Clase de excepcion propia - Hereda de Value error
    pass


@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str


class Categoria:
    def __init__(self, nombre: str, descripcion: str = "") -> None:
        if not nombre.strip():  # verifica si esta vacio o son solo espacios en blanco
            raise DomainError("El nombre de la categoría no puede estar vacío")
        self._nombre = nombre.strip()
        self._descripcion = descripcion

    # estos property evitan setters
    # Mantiene la inmutabilidad lógica de la categoría: una vez creada, su nombre y #descripción no cambian.
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion


class ProductoCategoria:
    def __init__(
        self, producto: Producto, categoria: Categoria, es_principal: bool = False
    ) -> None:
        self._producto = (
            producto  # ! aca se crea la composicion Producto → ProductoCategoria
        )
        self._categoria = categoria
        self._es_principal = es_principal

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal


class Producto(ABC):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        unidad_venta: UnidadMedida | None,
        categoria_principal: Categoria,
        habilitado: bool = True,
    ) -> None:

        # Atributos internos 
        self._nombre = nombre
        self._precio_base = precio_base
        self._stock_cantidad = stock_cantidad
        self._habilitado = habilitado
        self._unidad_venta = unidad_venta
        self._clasificaciones: list[ProductoCategoria] = [] # * es una lista con las categorias

        # ! Crea la clasificación principal (composición)
        principal = ProductoCategoria(self, categoria_principal, es_principal=True)
        self._clasificaciones.append(principal)

    # Properties públicas (UML: +)
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self) -> UnidadMedida | None:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self) -> str:
        if self._unidad_venta is None:
            return f"$ {self._precio_base:.2f}"
        return f"$ {self._precio_base:.2f} / {self._unidad_venta.simbolo}" # el simbolo sale de UnidadMedida

    @property
    def categorias(self) -> tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    @property
    def categoria_principal(self) -> Categoria:
        for vinculo in self._clasificaciones:
            if vinculo.es_principal:
                return vinculo.categoria
        raise RuntimeError("No hay categoría principal")
