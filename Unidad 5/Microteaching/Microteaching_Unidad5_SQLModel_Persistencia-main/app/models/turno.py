from datetime import date, time
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.paciente import Paciente


class TurnoBase(SQLModel):
    """Campos comunes a todas las variantes del turno (no es tabla)."""

    fecha: date
    hora: time
    profesional: str = Field(max_length=60)
    motivo: str = Field(max_length=200)


class Turno(TurnoBase, table=True):
    """Modelo de tabla: representa el turno persistido en PostgreSQL."""

    id: Optional[int] = Field(default=None, primary_key=True)

    # pendiente -> confirmado -> atendido, o pendiente/confirmado -> cancelado
    estado: str = Field(default="pendiente", max_length=20)

    paciente_id: int = Field(foreign_key="paciente.id")
    paciente: Optional["Paciente"] = Relationship(back_populates="turnos")
