from datetime import datetime, timezone
from typing import TYPE_CHECKING

from app.producto_categoria.model import ProductoCategoria
from sqlalchemy import ARRAY, Column, DateTime, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.categoria.model import Categoria
    
    
class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str = Field(
        min_length=2,
        max_length=150,
        sa_column=Column(String(150), nullable=False)
    )

    descripcion: str | None = None

    precio_base: float = Field(ge=0)

    imagenes_url: list[str] | None = Field(
        default=None,
        sa_column=Column(ARRAY(String))
    )

    disponible: bool = Field(default=True)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )

    categorias: list["Categoria"] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoria
    )
