from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel


class ProductoCategoria(SQLModel, table=True):
    producto_id: int | None = Field(
        default=None,
        foreign_key="producto.id",
        primary_key=True
    )
    categoria_id: int | None = Field(
        default=None,
        foreign_key="categoria.id",
        primary_key=True
    )

class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str = Field(min_length=2)
    descripcion: str = Field(min_length=5)
    precio: float = Field(gt=0)
    imagen_url: list[str] | None = Field(default=None, sa_column=Column(JSON))
    # imagen_url: str = Field(min_length=1)
    disponible: bool = True

    categorias: list["Categoria"] = Relationship( # type: ignore
        back_populates="productos",
        link_model=ProductoCategoria
    )

Producto.model_rebuild()