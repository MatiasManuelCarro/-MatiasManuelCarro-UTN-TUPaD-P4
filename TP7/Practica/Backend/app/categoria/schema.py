from datetime import datetime

from sqlmodel import SQLModel


class CategoriaCreate(SQLModel):
    nombre: str
    descripcion: str = "0"


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
