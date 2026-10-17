from pydantic import field_validator
from sqlmodel import Field, SQLModel

from app.models.producto import ProductoBase


class ProductoCreate(ProductoBase):

    @field_validator("nombre")
    def validar_nombre(cls, v):
        # RN-02: obligatorio, min_length=1, no solo espacios
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios.")
        return v.strip()


class ProductoUpdate(SQLModel):
    # Opcional: Se usa si en el futuro se implementa PATCH (actualización parcial)
    nombre: str | None = None
    categoria: str | None = Field(None, regex=r"^[A-Z]{3}-\d{2}$")
    precio: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    stock_minimo: int | None = Field(None, ge=0)
    activo: bool | None = None
    
    @field_validator("nombre")
    def validar_nombre_update(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios.")
        return v.strip()


class ProductoPublic(ProductoBase):
    id: int
    activo: bool | None

class ProductoStockResponse(SQLModel):
    stock: int
    bajo_stock_minimo: bool
    activo: bool
