from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

router = APIRouter(prefix="/turnos")

@router.get("")
def get_turnos():
    return load_json("turnos")

@router.post("")
def crear_turno(turno: dict[str, object]):
    turnos = load_json("turnos")
    nuevo_id = max([t["id"] for t in turnos], default=0) + 1
    turno["id"] = nuevo_id
    turno["estado"] = turno.get("estado", "PROGRAMADO")
    turnos.append(turno)
    save_json("turnos", turnos)
    return turno

@router.put("/{turno_id}")
def modificar_turno(turno_id: int, cambios: dict[str, object]):
    turnos = load_json("turnos")
    turno = find_by_id(turnos, turno_id)
    if not turno:
        raise HTTPException(404, "Turno no encontrado")
    turno.update(cambios)
    save_json("turnos", turnos)
    return turno
