from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.modules.productos.model import ProductoCategoria

if TYPE_CHECKING:
    from app.modules.productos.model import Producto



class Categoria(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False, min_length=3)
    descripcion: str | None = Field(default=None)
    activo: bool = Field(default=True, nullable=False)
    anulado_at: datetime | None = Field(default=None, nullable=True)
    
    productos: list["Producto"] = Relationship(back_populates="categorias", link_model=ProductoCategoria) 
