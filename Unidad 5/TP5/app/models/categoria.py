from sqlmodel import Field, SQLModel


# Base compartida 
class CategoriaBase(SQLModel):
    codigo: str = Field(regex=r"^[A-Z]{3}-\d{2}$", index=True)
    descripcion: str = Field(min_length=3)
    activo: bool = True

# Tabla persistente
class Categoria(CategoriaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


