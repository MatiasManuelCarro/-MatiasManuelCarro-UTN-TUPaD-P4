from sqlmodel import Field, SQLModel

from app.models.proveedor import ProveedorBase


class ProveedorCreate(ProveedorBase):
    pass

class ProveedorPublic(ProveedorBase):
    id: int

class ProveedorUpdate(SQLModel):
    codigo: str | None = Field(default=None, min_length=1)
    razon_social: str | None = Field(default=None, min_length=3)
    cuit: str | None = Field(default=None, min_length=11, max_length=15)
    email: str | None = Field(default=None)
    telefono: str | None = Field(default=None)
    activo: bool | None = Field(default=None)
