from sqlmodel import Field, SQLModel

# Base compartida 
class ProveedorBase(SQLModel):
    codigo: str = Field(min_length=1, index=True)
    razon_social: str = Field(min_length=3)
    cuit: str = Field(min_length=11, max_length=15)
    email: str = Field(default="")
    telefono: str = Field(default="")
    activo: bool = True

# Tabla persistente
class Proveedor(ProveedorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# POST
class ProveedorCreate(ProveedorBase):
    pass

# PATCH
class ProveedorUpdate(SQLModel):
    codigo: str | None = Field(default=None, min_length=1)
    razon_social: str | None = Field(default=None, min_length=3)
    cuit: str | None = Field(default=None, min_length=11, max_length=15)
    email: str | None = None
    telefono: str | None = None
    activo: bool | None = None

# GET
class ProveedorRead(ProveedorBase):
    id: int
