from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel


class ProductoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=100)
    descripcion: str = Field(min_length=3, max_length=255)
    precio: Decimal = Field(ge=0, decimal_places=2)
    stock_cantidad: Decimal = Field(ge=0, decimal_places=3)
    disponible: bool = True
    activo: bool = True
    anulado_at: datetime

class ProductoCreate(ProductoBase):
    categoria_ids: list[int] = []

class ProductoUpdate(SQLModel):
    nombre: str | None = Field(default = None, min_length=3, max_length=100)
    descripcion: str | None = Field(default=None, min_length= 3, max_length=255)
    precio: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    stock_cantidad: Decimal = Field(default= None, ge=0, decimal_places=3)
    disponible: bool = Field(default=True)