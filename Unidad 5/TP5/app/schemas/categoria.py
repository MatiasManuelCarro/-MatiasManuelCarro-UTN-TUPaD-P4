from sqlmodel import Field, SQLModel

from app.models.categoria import CategoriaBase


class CategoriaCreate(CategoriaBase):
    pass

class CategoriaPublic(CategoriaBase):
    id: int
    activo: bool | None


class CategoriaUpdate(SQLModel):
    codigo: str | None = Field(None, regex=r"^[A-Z]{3}-\d{2}$")
    descripcion: str | None = Field(None, min_length=3)
    activo: bool | None = None


class CategoriaRead(CategoriaBase):
    id: int
