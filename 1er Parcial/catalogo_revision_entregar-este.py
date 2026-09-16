from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class DomainError(ValueError):
    pass


class Exportable(Protocol):
    def exportar(self) -> str:
        pass


def exportar_catalogo(items: list[Exportable]) -> list[str]:
    exportado: list[str] = []
    for idx, item in enumerate(items):
        try:
            exportado.append(item.exportar())
        except Exception as e:
            tipo = type(item).__name__
            raise DomainError(
                f"Error exportando item con indice: {idx}, tipo: {tipo}: {e}"
            ) from e
    return exportado


@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str


class Categoria:
    def __init__(self, nombre: str, descripcion: str = "") -> None:
        if not nombre.strip():
            raise DomainError("El nombre de la categoría no puede estar vacío")
        self._nombre = nombre.strip()
        self._descripcion = descripcion

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
        self._producto = producto
        self._categoria = categoria
        self._es_principal = es_principal

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal

    def _marcar_principal(self, valor: bool) -> None:
        self._es_principal = valor


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

        if not nombre.strip():
            raise DomainError("El nombre del producto no puede estar vacío")
        if precio_base < 0:
            raise DomainError("El precio base no puede ser negativo")
        if stock_cantidad < 0:
            raise DomainError("El stock no puede ser negativo")

        self._nombre = nombre
        self._precio_base = precio_base
        self._stock_cantidad = stock_cantidad
        self._habilitado = habilitado
        self._unidad_venta = unidad_venta
        self._clasificaciones: list[ProductoCategoria] = []

        principal = ProductoCategoria(self, categoria_principal, es_principal=True)
        self._clasificaciones.append(principal)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def stock_cantidad(self) -> float:
        return self._stock_cantidad

    def ajustar_stock(self, cambio: float) -> None:
        nuevo = self._stock_cantidad + cambio
        if nuevo < 0:
            raise DomainError("El stock no puede ser negativo")
        self._stock_cantidad = nuevo

    def set_stock(self, cantidad: float) -> None:
        if cantidad < 0:
            raise DomainError("El stock no puede ser negativo")
        self._stock_cantidad = cantidad

    @property
    def unidad_venta(self) -> UnidadMedida | None:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_cantidad > 0

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        raise NotImplementedError

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    def clasificar_en(self, categoria: Categoria, es_principal: bool = False) -> None:
        for vinculo in self._clasificaciones:
            if vinculo.categoria is categoria:
                raise DomainError("El producto ya está clasificado en esta categoría")

        if es_principal:
            actual = next((v for v in self._clasificaciones if v.es_principal), None)
            if actual:
                actual._marcar_principal(False)

        nuevo = ProductoCategoria(self, categoria, es_principal)
        self._clasificaciones.append(nuevo)

    def marcar_categoria_principal(self, categoria: Categoria) -> None:
        vinculo = next(
            (v for v in self._clasificaciones if v.categoria is categoria), None
        )
        if vinculo is None:
            raise DomainError("El producto no está clasificado en esa categoría")

        actual = next((v for v in self._clasificaciones if v.es_principal), None)
        if actual:
            actual._marcar_principal(False)

        vinculo._marcar_principal(True)

    @property
    def precio_publicado(self) -> str:
        precio = self.precio_base
        if self._unidad_venta is None:
            return f"$ {precio:.2f}"
        return f"$ {precio:.2f} / {self._unidad_venta.simbolo}"

    @property
    def categorias(self) -> tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    @property
    def categoria_principal(self) -> Categoria:
        for vinculo in self._clasificaciones:
            if vinculo.es_principal:
                return vinculo.categoria
        raise RuntimeError("No hay categoría principal")

    @abstractmethod
    def exportar(self) -> str:
        raise NotImplementedError


class ProductoSimple(Producto):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        unidad_venta: UnidadMedida | None,
        categoria_principal: Categoria,
        habilitado: bool = True,
    ) -> None:

        if precio_base < 1 or precio_base != int(precio_base):
            raise DomainError(
                "precio_base debe ser entero y no puede ser negativo en ProductoSimple"
            )

        super().__init__(
            nombre,
            precio_base,
            stock_cantidad,
            unidad_venta,
            categoria_principal,
            habilitado,
        )

    def cambiar_precio(self, nuevo_precio: float) -> None:
        if nuevo_precio <= 0:
            raise DomainError("precio_base debe ser > 0 en ProductoSimple")
        self._precio_base = float(nuevo_precio)

    def precio_final(self, cantidad: float) -> float:
        if cantidad < 1 or cantidad != int(cantidad):
            raise DomainError("La cantidad debe ser entera y >= 1 en ProductoSimple")
        return self._precio_base * cantidad

    def exportar(self) -> str:
        return f"PROD|{self.nombre}|{self.precio_base}"


class ProductoPorPeso(Producto):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        unidad_venta: UnidadMedida | None,
        categoria_principal: Categoria,
        habilitado: bool = True,
    ) -> None:

        if precio_base <= 0:
            raise DomainError("precio_base debe ser > 0 para ProductoPorPeso")

        super().__init__(
            nombre,
            precio_base,
            stock_cantidad,
            unidad_venta,
            categoria_principal,
            habilitado,
        )

    def cambiar_precio(self, nuevo_precio: float) -> None:
        if nuevo_precio <= 0:
            raise DomainError("precio_base debe ser > 0 para ProductoPorPeso")
        self._precio_base = float(nuevo_precio)

    def precio_final(self, cantidad: float) -> float:
        if cantidad <= 0:
            raise DomainError("La cantidad debe ser > 0 en ProductoPorPeso")
        return round(self._precio_base * cantidad, 2)

    def exportar(self) -> str:
        if self.unidad_venta is None:
            raise DomainError("ProductoPorPeso requiere unidad_venta para exportar")
        return f"PROD_PESO|{self.nombre}|{self.precio_base}|{self.unidad_venta.simbolo}"


class ProductoCombo(Producto):
    def __init__(
        self,
        nombre: str,
        componentes: list[Producto],
        descuento: float,
        unidad_venta: UnidadMedida | None,
        categoria_principal: Categoria,
        habilitado: bool = True,
    ) -> None:

        if len(componentes) < 2:
            raise DomainError("Un ProductoCombo debe tener al menos 2 componentes")

        for comp in componentes:
            if not isinstance(comp, Producto):
                raise DomainError(
                    "Todos los componentes de un combo deben ser Productos"
                )

        if not (0 <= descuento < 1):
            raise DomainError("El descuento debe estar en el rango [0, 1)")

        super().__init__(
            nombre,
            precio_base=0.0,
            stock_cantidad=0.0,
            unidad_venta=unidad_venta,
            categoria_principal=categoria_principal,
            habilitado=habilitado,
        )

        self._componentes = list(componentes)
        self._descuento: float = descuento

    @property
    def precio_base(self) -> float:
        return sum(comp.precio_base for comp in self._componentes)

    @property
    def disponible(self) -> bool:
        componentes_disponibles = all(comp.disponible for comp in self._componentes)
        return self._habilitado and componentes_disponibles

    @property
    def componentes(self) -> tuple[Producto, ...]:
        return tuple(self._componentes)

    def precio_final(self, cantidad: float) -> float:
        if cantidad < 1 or cantidad != int(cantidad):
            raise DomainError("La cantidad debe ser un entero >= 1 para ProductoCombo")

        subtotal = sum(p.precio_final(1) for p in self._componentes)
        total_con_descuento = subtotal * (1 - self._descuento)
        return total_con_descuento * cantidad

    def exportar(self) -> str:
        return f"COMBO|{self.nombre}|{len(self._componentes)}"


class ProductoDestacado:
    def __init__(self, producto: Producto, orden_vidriera: int) -> None:
        self._producto = producto
        self._orden_vidriera = orden_vidriera

    @property
    def orden_vidriera(self) -> int:
        return self._orden_vidriera

    @property
    def producto(self) -> Producto:
        return self._producto

    def exportar(self) -> str:
        return f"DEST|{self._producto.nombre}|{self._orden_vidriera}"
