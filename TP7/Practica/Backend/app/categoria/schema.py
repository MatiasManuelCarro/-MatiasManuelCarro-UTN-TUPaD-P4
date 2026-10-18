from datetime import datetime

from sqlmodel import Field, SQLModel


class CategoriaCreate(SQLModel):
    nombre: str = Field(min_length=1)
    descripcion: str = ""


class CategoriaUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None


class CategoriaPublic(SQLModel):
    id: int
    nombre: str
    descripcion: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CategoriaPaginatedResponse(SQLModel):
    total: int
    items: list[CategoriaPublic]