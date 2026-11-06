from datetime import datetime
from typing import Annotated

from sqlmodel import Field, SQLModel


class CategoriaBase(SQLModel):
    nombre: Annotated[str, Field(min_length=3, max_length=100)]
    descripcion: str | None = Field(default=None, max_length=255)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaPublic(CategoriaBase):
    id: int
    activo: bool
    anulado_at: datetime | None

