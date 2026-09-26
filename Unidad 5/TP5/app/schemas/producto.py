from sqlmodel import Field, SQLModel

from app.models.producto import ProductoBase


class ProductoCreate(ProductoBase):
    pass  # Exige todos los campos obligatorios de Base


class ProductoUpdate(SQLModel):
    # Opcional: Se usa si en el futuro se implementa PATCH (actualización parcial)
    nombre: str | None = None
    categoria: str | None = Field(None, pattern=r"^[A-Z]{3}-\d{2}$")
    precio: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    stock_minimo: int | None = Field(None, ge=0)
    activo: bool | None = None


class ProductoPublic(ProductoBase):
    id: int
    activo: bool | None

class ProductoStockResponse(ProductoBase):
    stock: int
    bajo_stock_minimo: bool
    activo: bool
