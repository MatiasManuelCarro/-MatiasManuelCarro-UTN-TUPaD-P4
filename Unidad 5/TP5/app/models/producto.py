from sqlmodel import Field, SQLModel


# Base compartida 
class ProductoBase(SQLModel):
    nombre: str = Field(index=True)
    categoria: str = Field(regex=r"^[A-Z]{3}-\d{2}$")
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    stock_minimo: int = Field(ge=0)
    activo: bool = True

# Tabla persistencia
class Producto(ProductoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


