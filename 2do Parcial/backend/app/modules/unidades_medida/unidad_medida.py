from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.productos.model import Producto


class TipoUnidad(str, Enum):
    PESO = "peso"
    VOLUMEN = "volumen"
    CONTABLE = "contable"


class UnidadMedida(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False, unique=True)
    simbolo: str = Field(nullable=False, unique=True)
    tipo: TipoUnidad = Field(nullable=False)
    
    productos: list["Producto"] = Relationship( 
        back_populates="unidad_venta"
    )