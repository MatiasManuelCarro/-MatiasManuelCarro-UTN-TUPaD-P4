from typing import Optional

from database import SessionDep
from fastapi import APIRouter, status

from app.schemas.paciente import (
    PacienteConTurnos,
    PacienteCreate,
    PacientePublic,
    PacienteUpdate,
)
from app.service import paciente_service

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/", response_model=PacientePublic, status_code=status.HTTP_201_CREATED)
def crear_paciente(paciente: PacienteCreate, session: SessionDep):
    return paciente_service.crear_paciente(session, paciente)


@router.get("/", response_model=list[PacientePublic])
def listar_pacientes(
    session: SessionDep,
    skip: int = 0,
    limit: int = 20,
    activo: bool | None = None,
):
    return paciente_service.listar_pacientes(session, skip, limit, activo)


@router.get("/{paciente_id}", response_model=PacienteConTurnos)
def obtener_paciente(paciente_id: int, session: SessionDep):
    return paciente_service.obtener_paciente(session, paciente_id)


@router.patch("/{paciente_id}", response_model=PacientePublic)
def actualizar_paciente(paciente_id: int, paciente: PacienteUpdate, session: SessionDep):
    return paciente_service.actualizar_paciente(session, paciente_id, paciente)


@router.patch("/{paciente_id}/desactivar", response_model=PacientePublic)
def desactivar_paciente(paciente_id: int, session: SessionDep):
    return paciente_service.desactivar_paciente(session, paciente_id)
