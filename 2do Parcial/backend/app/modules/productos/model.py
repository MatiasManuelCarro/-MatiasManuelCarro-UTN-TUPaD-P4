from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from app.modules.unidades_medida.model import UnidadMedida
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.categorias.model import Categoria



class ProductoCategoria(SQLModel, table=True):
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)
    es_principal: bool = Field(default=False, nullable=False)


class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    unidad_venta_id: int = Field(nullable=False, foreign_key="unidad_medida.id")
    nombre: str = Field(nullable=False)
    descripcion: str | None = Field(default=None)
    precio_base: Decimal = Field(ge=0, decimal_places=2)
    stock_cantidad: Decimal = Field(default=0, ge=0, decimal_places=3)
    disponible: bool = Field(default=True, nullable=False)
    activo: bool = Field(default=True, nullable=False)
    anulado_at: datetime | None = Field(default=None)
    
    categorias: list["Categoria"] = Relationship( 
        back_populates="productos",
        link_model=ProductoCategoria
    )
    
    unidad_venta: "UnidadMedida" = Relationship( 
        back_populates="productos"
    )

