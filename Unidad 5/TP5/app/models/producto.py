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

# POST
class ProductoCreate(ProductoBase):
    pass
    # Usa todos los campos obligatorios de ProductoBase

# PATCH
class ProductoUpdate(SQLModel):
    nombre: str | None = None
    categoria: str | None = Field(default=None, regex=r"^[A-Z]{3}-\d{2}$")
    precio: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    stock_minimo: int | None = Field(default=None, ge=0)
    activo: bool | None = None

# 5. GET
class ProductoRead(ProductoBase):
    id: int

# 6. Respuesta específica
class ProductoStockResponse(SQLModel):
    stock: int
    bajo_stock_minimo: bool
    activo: bool
