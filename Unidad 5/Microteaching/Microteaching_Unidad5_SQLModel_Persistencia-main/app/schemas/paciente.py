from datetime import date, time
from typing import Optional

from sqlmodel import SQLModel

from app.models.paciente import PacienteBase


class PacienteCreate(PacienteBase):
    """Esquema de entrada para crear un paciente. No incluye id ni activo."""

    obra_social: Optional[str] = None


class PacientePublic(PacienteBase):
    """Esquema de salida. Nunca expone obra_social."""

    id: int
    activo: bool


class PacienteUpdate(SQLModel):
    """Esquema para PATCH: todos los campos opcionales."""

    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    obra_social: Optional[str] = None
    fecha_nacimiento: Optional[date] = None


class TurnoResumen(SQLModel):
    """Vista reducida de un turno, usada al anidarlo dentro del paciente."""

    id: int
    fecha: date
    hora: time
    profesional: str
    estado: str


class PacienteConTurnos(PacientePublic):
    """Esquema de salida para GET /pacientes/{id}: incluye sus turnos."""

    turnos: list[TurnoResumen] = []
