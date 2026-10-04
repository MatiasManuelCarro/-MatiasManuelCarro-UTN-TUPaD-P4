from sqlmodel import Field, SQLModel

from app.categoria.schema import CategoriaPublic


class ProductoBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=5, max_length=255)
    precio: float = Field(gt=0)
    imagen_url: list[str]
    disponible: bool = True


class ProductoCreate(ProductoBase):
    categoria_ids: list[int] = []


class ProductoUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, min_length=5, max_length=255)
    precio: float | None = Field(default=None, gt=0)
    imagen_url: list[str] | None = None
    disponible: bool | None = None
    categoria_ids: list[int] | None = None


class ProductoPublic(ProductoBase):
    id: int
    categorias: list[CategoriaPublic] = []
