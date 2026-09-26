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

