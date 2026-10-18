from datetime import UTC, datetime
from typing import TYPE_CHECKING

from app.producto_categoria.model import ProductoCategoria
from sqlalchemy import Column, DateTime, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.producto.model import Producto

class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str = Field(
        min_length=1,
        max_length=100,
        sa_column=Column(String(100), unique=True, nullable=False)
    )

    descripcion: str = Field(
    default="",
    sa_column=Column(String, nullable=False)
    )

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )

    productos: list["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria
    )
