from sqlmodel import Field, Relationship, SQLModel

from app.producto.model import ProductoCategoria


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2)
    descripcion: str = Field(min_length=5)
    
    productos: list["Producto"] = Relationship(back_populates="categorias", link_model=ProductoCategoria) # type: ignore  # noqa: F821
