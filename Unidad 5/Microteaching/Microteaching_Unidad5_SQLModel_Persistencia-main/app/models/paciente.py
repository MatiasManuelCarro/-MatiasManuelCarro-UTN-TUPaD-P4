from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.turno import Turno


class PacienteBase(SQLModel):
    """Campos comunes a todas las variantes del paciente (no es tabla)."""

    nombre: str = Field(index=True, min_length=2, max_length=50)
    apellido: str = Field(index=True, min_length=2, max_length=50)
    dni: str = Field(index=True, unique=True, min_length=7, max_length=10)
    telefono: str = Field(max_length=20)
    fecha_nacimiento: Optional[date] = None


class Paciente(PacienteBase, table=True):
    """Modelo de tabla: representa la entidad persistida en PostgreSQL."""

    id: Optional[int] = Field(default=None, primary_key=True)

    # Campo interno/sensible: se acepta al crear, pero nunca se devuelve
    # en el modelo público (PacientePublic).
    obra_social: Optional[str] = Field(default=None, max_length=50)

    # Baja lógica en lugar de borrado físico.
    activo: bool = Field(default=True)

    turnos: list["Turno"] = Relationship(back_populates="paciente")
