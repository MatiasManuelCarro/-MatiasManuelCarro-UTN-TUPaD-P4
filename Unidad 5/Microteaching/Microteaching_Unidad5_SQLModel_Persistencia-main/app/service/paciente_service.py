"""
Lógica de negocio de Pacientes: es la única capa que controla
transacciones (add/commit/refresh) y decide cuándo confirmar o
rechazar una operación.
"""

from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteUpdate


def crear_paciente(session: Session, data: PacienteCreate) -> Paciente:
    existe = session.exec(select(Paciente).where(Paciente.dni == data.dni)).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un paciente con DNI {data.dni}",
        )

    nuevo_paciente = Paciente(**data.model_dump())
    session.add(nuevo_paciente)
    session.commit()
    session.refresh(nuevo_paciente)
    return nuevo_paciente


def listar_pacientes(
    session: Session,
    skip: int = 0,
    limit: int = 20,
    activo: Optional[bool] = None,
) -> list[Paciente]:
    query = select(Paciente)
    if activo is not None:
        query = query.where(Paciente.activo == activo)
    query = query.offset(skip).limit(limit)
    return list(session.exec(query).all())


def obtener_paciente(session: Session, paciente_id: int) -> Paciente:
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
    return paciente


def actualizar_paciente(session: Session, paciente_id: int, data: PacienteUpdate) -> Paciente:
    paciente = obtener_paciente(session, paciente_id)

    cambios = data.model_dump(exclude_unset=True)
    paciente.sqlmodel_update(cambios)

    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente


def desactivar_paciente(session: Session, paciente_id: int) -> Paciente:
    """Baja lógica: no borra al paciente, lo marca inactivo."""
    paciente = obtener_paciente(session, paciente_id)

    if not paciente.activo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El paciente ya está inactivo")

    paciente.activo = False
    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente
