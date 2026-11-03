from datetime import datetime
from typing import TYPE_CHECKING

from app.modules.productos.model import ProductoCategoria
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.productos.model import Producto



class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    descripcion: str | None = Field(default=None)
    activo: bool = Field(default=True, nullable=False)
    anulado_at: datetime | None = Field(default=None, nullable=True)
    
    productos: list["Producto"] = Relationship(back_populates="categorias", link_model=ProductoCategoria) 
