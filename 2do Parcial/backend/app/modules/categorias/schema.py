

from datetime import datetime

from sqlmodel import Field, SQLModel


class CategoriaCreate(SQLModel):
    nombre: str = Field(min_lenght=3)
    descripcion: str | None  = Field(default=None, max_length=255)

class CategoriaUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=3, max_length=100)
    descripcion: str | None = Field(default=None, min_length=5, max_length=255)


class CategoriaPublic(SQLModel):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
    anulado_at: datetime | None