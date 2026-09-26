"""
Lógica de negocio de Turnos: valida al paciente, las reglas de
agenda (sin superposición, sin fechas pasadas) y controla los
cambios de estado (confirmar / cancelar).
"""

from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.paciente import Paciente
from app.models.turno import Turno
from app.schemas.turno import TurnoCreate, TurnoUpdate

ESTADOS_FINALES = {"cancelado", "atendido"}


def crear_turno(session: Session, data: TurnoCreate) -> Turno:
    paciente = session.get(Paciente, data.paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El paciente indicado no existe")
    if not paciente.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pueden asignar turnos a un paciente inactivo",
        )

    if data.fecha < date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pueden crear turnos en una fecha pasada")

    turnos_mismo_horario = session.exec(
        select(Turno).where(
            Turno.profesional == data.profesional,
            Turno.fecha == data.fecha,
            Turno.hora == data.hora,
        )
    ).all()
    if any(t.estado not in ESTADOS_FINALES for t in turnos_mismo_horario):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El profesional ya tiene un turno vigente en ese horario",
        )

    nuevo_turno = Turno(**data.model_dump())
    session.add(nuevo_turno)
    session.commit()
    session.refresh(nuevo_turno)
    return nuevo_turno


def listar_turnos(
    session: Session,
    skip: int = 0,
    limit: int = 20,
    estado: Optional[str] = None,
    paciente_id: Optional[int] = None,
    fecha: Optional[date] = None,
) -> list[Turno]:
    query = select(Turno)
    if estado is not None:
        query = query.where(Turno.estado == estado)
    if paciente_id is not None:
        query = query.where(Turno.paciente_id == paciente_id)
    if fecha is not None:
        query = query.where(Turno.fecha == fecha)
    query = query.offset(skip).limit(limit)
    return list(session.exec(query).all())


def obtener_turno(session: Session, turno_id: int) -> Turno:
    turno = session.get(Turno, turno_id)
    if not turno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turno no encontrado")
    return turno


def actualizar_turno(session: Session, turno_id: int, data: TurnoUpdate) -> Turno:
    turno = obtener_turno(session, turno_id)

    if turno.estado in ESTADOS_FINALES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede modificar un turno cancelado o ya atendido",
        )

    cambios = data.model_dump(exclude_unset=True)
    turno.sqlmodel_update(cambios)

    session.add(turno)
    session.commit()
    session.refresh(turno)
    return turno


def confirmar_turno(session: Session, turno_id: int) -> Turno:
    turno = obtener_turno(session, turno_id)
    if turno.estado != "pendiente":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Solo se puede confirmar un turno pendiente")

    turno.estado = "confirmado"
    session.add(turno)
    session.commit()
    session.refresh(turno)
    return turno


def cancelar_turno(session: Session, turno_id: int) -> Turno:
    turno = obtener_turno(session, turno_id)
    if turno.estado in ESTADOS_FINALES:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El turno ya está cancelado o atendido")

    turno.estado = "cancelado"
    session.add(turno)
    session.commit()
    session.refresh(turno)
    return turno
