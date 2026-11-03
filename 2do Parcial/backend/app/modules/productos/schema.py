from decimal import Decimal
from typing import Annotated

from app.modules.categorias.schema import CategoriaPublic
from app.modules.unidades_medida.model import TipoUnidad
from sqlmodel import Field, SQLModel


class UnidadMedidaPublic(SQLModel):
    id: int
    nombre: str
    simbolo: str
    tipo: TipoUnidad


class ProductoBase(SQLModel):
    nombre: Annotated[str, Field(min_length=3, max_length=100)]
    descripcion: str | None  = Field(default=None, max_length=255)
    precio_base:Annotated[Decimal, Field(ge=0, decimal_places=2)]
    unidad_venta_id: int
    stock_cantidad: Annotated[Decimal ,Field(default=0, ge=0, decimal_places=3)]
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(SQLModel):
    nombre: Annotated[str ,Field(default=None, min_length=3, max_length=100)]
    descripcion: str | None = Field(default=None, min_length=3, max_length=255)
    precio_base: Annotated [Decimal | None, Field(default=None, ge=0, decimal_places=2)]
    unidad_venta_id: int
    stock_cantidad: Annotated [Decimal, Field(default=None, ge=0, decimal_places=3)]
    disponible: bool | None = Field(default=True)



class ProductoPublic(ProductoBase):
    id: int
    unidad_venta: UnidadMedidaPublic
    categorias: list[CategoriaPublic]
    hay_stock: bool
