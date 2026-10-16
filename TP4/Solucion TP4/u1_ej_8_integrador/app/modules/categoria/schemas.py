from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    codigo: str = Field(..., pattern=r"^[A-Z]{3}-\d{2}$", example="MUE-01")
    descripcion: str = Field(..., min_length=3, example="Muebles de Oficina")
    activo: bool = True


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    codigo: str | None = Field(None, pattern=r"^[A-Z]{3}-\d{2}$")
    descripcion: str | None = Field(None, min_length=3)
    activo: bool | None = None


class CategoriaRead(CategoriaBase):
    id: int
