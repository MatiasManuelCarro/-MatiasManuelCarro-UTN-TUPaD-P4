from datetime import date
from typing import Optional

from fastapi import APIRouter, status

from database import SessionDep
from app.schemas.turno import TurnoCreate, TurnoPublic, TurnoUpdate
from app.service import turno_service

router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.post("/", response_model=TurnoPublic, status_code=status.HTTP_201_CREATED)
def crear_turno(turno: TurnoCreate, session: SessionDep):
    return turno_service.crear_turno(session, turno)


@router.get("/", response_model=list[TurnoPublic])
def listar_turnos(
    session: SessionDep,
    skip: int = 0,
    limit: int = 20,
    estado: Optional[str] = None,
    paciente_id: Optional[int] = None,
    fecha: Optional[date] = None,
):
    return turno_service.listar_turnos(session, skip, limit, estado, paciente_id, fecha)


@router.get("/{turno_id}", response_model=TurnoPublic)
def obtener_turno(turno_id: int, session: SessionDep):
    return turno_service.obtener_turno(session, turno_id)


@router.patch("/{turno_id}", response_model=TurnoPublic)
def actualizar_turno(turno_id: int, turno: TurnoUpdate, session: SessionDep):
    return turno_service.actualizar_turno(session, turno_id, turno)


@router.patch("/{turno_id}/confirmar", response_model=TurnoPublic)
def confirmar_turno(turno_id: int, session: SessionDep):
    return turno_service.confirmar_turno(session, turno_id)


@router.patch("/{turno_id}/cancelar", response_model=TurnoPublic)
def cancelar_turno(turno_id: int, session: SessionDep):
    return turno_service.cancelar_turno(session, turno_id)
