from sqlmodel import Field, SQLModel


class ProductoCreate(SQLModel):
    nombre: str = Field(min_length=2)
    descripcion: str | None = None
    precio_base: float = Field(ge=0)
    disponible: bool = True


class ProductoUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=2)
    descripcion: str | None = None
    precio_base: float | None = Field(default=None, ge=0)
    disponible: bool | None = None


class ProductoPublic(SQLModel):
    id: int
    nombre: str
    descripcion: str | None
    precio_base: float
    disponible: bool

    class Config:
        orm_mode = True
