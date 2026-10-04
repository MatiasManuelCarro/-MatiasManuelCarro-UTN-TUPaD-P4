
from sqlmodel import Field, SQLModel


class CategoriaCreate(SQLModel):
    nombre: str = Field(min_length=2)
    descripcion: str = Field(min_length=5)


class CategoriaUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, min_length=5, max_length=255)


class CategoriaPublic(SQLModel):
    id: int
    nombre: str
    descripcion: str
