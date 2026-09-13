from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class DomainError(ValueError):  # Clase de excepcion propia - Hereda de Value error
    pass


class Exportable(Protocol):
    def exportar(self) -> str:
        pass


def exportar_catalogo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]


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

    # TODO revisar logica
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

        # Validaciones
        if not nombre.strip():
            raise DomainError("El nombre del producto no puede estar vacío")

        if precio_base < 0:
            raise DomainError("El precio base no puede ser negativo")

        if stock_cantidad < 0:
            raise DomainError("El stock no puede ser negativo")

        # Atributos internos
        self._nombre = nombre
        self._precio_base = precio_base
        self._stock_cantidad = stock_cantidad
        self._habilitado = habilitado
        self._unidad_venta = unidad_venta
        self._clasificaciones: list[
            ProductoCategoria
        ] = []  # * es una lista con las categorias

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

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        raise NotImplementedError

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    # TODO Revisar esta logica
    def clasificar_en(self, categoria: Categoria, es_principal: bool = False) -> None:

        # No se puede clasificar dos veces en la misma categoría
        for vinculo in self._clasificaciones:
            if vinculo.categoria is categoria:
                raise DomainError("El producto ya está clasificado en esta categoría")

        if es_principal:
            actual = next((v for v in self._clasificaciones if v.es_principal), None)
            if actual:
                actual._marcar_principal(False)

        nuevo = ProductoCategoria(self, categoria, es_principal)
        self._clasificaciones.append(nuevo)

    @property
    def precio_publicado(self) -> str:
        precio = self.precio_base
        if self._unidad_venta is None:
            return f"$ {precio:.2f}"
        return f"$ {precio:.2f} / {self._unidad_venta.simbolo}"  # el simbolo sale de UnidadMedida

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

        # ProductoSimple: precio_base debe ser entero y >= 1
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

        # ProductoPorPeso: precio_base > 0 y admite decimales
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

    def precio_final(self, cantidad: float) -> float:
        if cantidad <= 0:
            raise DomainError("La cantidad debe ser > 0 en ProductoPorPeso")
        # ProductoPorPeso redondea a 2 decimales
        return round(self._precio_base * cantidad, 2)

    def exportar(self) -> str:
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
            if not isinstance(comp, Producto): #solo verifica que se reciba un producto. no que tipo
                raise DomainError(
                    "Todos los componentes de un combo deben ser Productos"
                )

        if not (0 <= descuento < 1):
            raise DomainError("El descuento debe estar en el rango [0, 1)")

        # Inicializamos la clase padre.
        # Le pasamos 0 al precio_base y stock_cantidad base porque
        # vamos a sobreescribir cómo se comportan más abajo.
        super().__init__(
            nombre,
            precio_base=0.0,
            stock_cantidad=0.0,
            unidad_venta=unidad_venta,
            categoria_principal=categoria_principal,
            habilitado=habilitado,
        )

        self._componentes: list[Producto] = componentes
        self._descuento: float = descuento

    # --- DECISIÓN DE DISEÑO EXPLICADA ---
    # Decisión: El precio_base y la disponibilidad de un Combo no son datos estáticos.
    # Se derivan dinámicamente de sus componentes. Así, si un componente agota su stock
    # o cambia su precio, el combo se actualiza automáticamente.

    @property
    def precio_base(self) -> float:
        # El precio base del combo es la suma de los precios base de sus componentes
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


class ProductoDestacado:  # Ya no hereda de Producto
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
        # Exporta como Destacado pero delega los datos al producto que envuelve
        return f"DEST|{self._producto.nombre}|{self._orden_vidriera}"


# * DEPRECATED - REVISAR MAS TARDE
# class ProductoDestacado(Producto):
#     def __init__(
#         self,
#         nombre: str,
#         precio_base: float,
#         stock_cantidad: float,
#         unidad_venta: str | None,
#         categoria_principal: str,
#         orden_vidriera: int,
#         habilitado: bool = True,
#     ) -> None:
#         super().__init__(
#             nombre,
#             precio_base,
#             stock_cantidad,
#             unidad_venta,
#             categoria_principal,
#             habilitado,
#         )
#         self._orden_vidriera = orden_vidriera

#     @property
#     def orden_vidriera(self) -> int:
#         return self._orden_vidriera

#     def precio_final(self, cantidad: float) -> float:
#         if cantidad <= 0:
#             raise ValueError("Cantidad inválida, no puede ser negativa")
#         return self._precio_base * cantidad

#     def exportar(self) -> str:
#         return f"DEST|{self.nombre}|{self.orden_vidriera}"


# class ProductoCombo(Producto):
#     def __init__(
#         self,
#         nombre: str,
#         componentes: list[Producto],
#         descuento: float,
#         precio_base: float,
#         stock_cantidad: float,
#         unidad_venta: UnidadMedida | None,
#         categoria_principal: Categoria,
#         habilitado: bool = True,
#     ) -> None:

#         # Validación: mínimo 2 componentes
#         if len(componentes) < 2:
#             raise DomainError("Un ProductoCombo debe tener al menos 2 componentes")

#         # Validación: todos deben ser Productos
#         for comp in componentes:
#             if not isinstance(comp, Producto):
#                 raise DomainError(
#                     "Todos los componentes deben ser instancias de Producto"
#                 )

#         # Validación: descuento en [0, 1)
#         if not (0 <= descuento < 1):
#             raise DomainError("El descuento debe estar en el rango [0, 1)")

#         # Validación: precio_base del combo (decisión obligatoria)
#         if precio_base < 0:
#             raise DomainError("precio_base del combo debe ser >= 0")

#         super().__init__(
#             nombre,
#             precio_base,
#             stock_cantidad,
#             unidad_venta,
#             categoria_principal,
#             habilitado,
#         )

#         self._componentes: list[Producto] = componentes
#         self._descuento: float = descuento

#     @property
#     def componentes(self) -> tuple[Producto, ...]:
#         return tuple(self._componentes)

#     def precio_final(self, cantidad: float) -> float:
#         if cantidad < 1 or cantidad != int(cantidad):
#             raise DomainError("La cantidad debe ser un entero >= 1 para ProductoCombo")

#         subtotal = sum(p.precio_final(1) for p in self._componentes)
#         total_con_descuento = subtotal * (1 - self._descuento)
#         return total_con_descuento * cantidad

#     def exportar(self) -> str:
#         return f"COMBO|{self.nombre}|{len(self._componentes)}"
