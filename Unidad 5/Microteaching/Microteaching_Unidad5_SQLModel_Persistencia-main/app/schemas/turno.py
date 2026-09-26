from datetime import date, time
from typing import Optional

from sqlmodel import SQLModel

from app.models.turno import TurnoBase


class TurnoCreate(TurnoBase):
    """Esquema de entrada para crear un turno. No incluye id ni estado."""

    paciente_id: int


class TurnoPublic(TurnoBase):
    """Esquema de salida."""

    id: int
    paciente_id: int
    estado: str


class TurnoUpdate(SQLModel):
    """Esquema para PATCH: reprogramar un turno (solo si sigue vigente)."""

    fecha: Optional[date] = None
    hora: Optional[time] = None
    profesional: Optional[str] = None
    motivo: Optional[str] = None
