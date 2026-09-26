from typing import Optional

from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    nombre: str = Field(..., example="Silla de Oficina")
    categoria: str = Field(..., pattern=r"^[A-Z]{3}-\d{2}$", example="MUE-01")
    precio: float = Field(gt=0, example=150.50)
    stock: int = Field(ge=0, example=20)
    stock_minimo: int = Field(ge=0, example=5)
    activo: bool = True


class ProductoCreate(ProductoBase):
    pass  # Exige todos los campos obligatorios de Base


class ProductoUpdate(BaseModel):
    # Opcional: Se usa si en el futuro se implementa PATCH (actualización parcial)
    nombre: str | None = None
    categoria: str | None = Field(None, pattern=r"^[A-Z]{3}-\d{2}$")
    precio: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    stock_minimo: int | None = Field(None, ge=0)
    activo: bool | None = None


class ProductoRead(ProductoBase):
    id: int  # Contrato de salida: siempre incluye el ID generado


class ProductoStockResponse(BaseModel):
    stock: int
    bajo_stock_minimo: bool
    activo: bool
