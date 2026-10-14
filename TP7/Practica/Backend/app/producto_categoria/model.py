from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class ProductoCategoria(SQLModel, table=True):
    producto_id: int = Field(primary_key=True, foreign_key="producto.id")
    categoria_id: int = Field(primary_key=True, foreign_key="categoria.id")

    es_principal: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
