from sqlmodel import Field, SQLModel


class ProductoCreate(SQLModel):
    nombre: str = Field(min_length=1)
    descripcion: str | None = None
    precio_base: float = Field(ge=0)
    imagenes_url: list[str] | None = None
    disponible: bool = True
    # asociacion N:M a categoria o categorias
    categorias: list[int] = []


class ProductoUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=2)
    descripcion: str | None = None
    precio_base: float | None = Field(default=None, ge=0)
    imagenes_url: list[str] | None = None
    disponible: bool | None = None
    
    # ASociar categorias al actualizar el producto
    categorias: list[int] | None = None


class ProductoPublic(SQLModel):
    id: int
    nombre: str
    descripcion: str | None
    precio_base: float
    imagenes_url: list[str] | None
    disponible: bool
    
    # Lista de IDs de categorías
    categorias: list[int]

    class Config:
        orm_mode = True

class ProductoPaginatedResponse(SQLModel):
    total: int
    items: list[ProductoPublic]
