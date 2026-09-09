from pydantic import BaseModel, Field


class ProveedorBase(BaseModel):
    codigo: str = Field(..., min_length=1)
    razon_social: str = Field(..., min_length=3)
    cuit: str = Field(..., min_length=11, max_length=15)
    email: str = Field(default="")
    telefono: str = Field(default="")
    activo: bool = Field(default=True)

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorRead(ProveedorBase):
    id: int

class ProveedorUpdate(ProveedorBase):
    codigo: str | None = Field(default=None, min_length=1)
    razon_social: str | None = Field(default=None, min_length=3)
    cuit: str | None = Field(default=None, min_length=11, max_length=15)
    email: str | None = Field(default=None)
    telefono: str | None = Field(default=None)
    activo: bool | None = Field(default=None)
