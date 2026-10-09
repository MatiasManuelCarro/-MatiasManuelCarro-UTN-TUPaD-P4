from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

router = APIRouter(prefix="/ambulancias")

@router.get("")
def get_ambulancias():
    return load_json("ambulancias")

@router.post("")
def crear_ambulancia(amb: dict[str, object]):
    ambulancias = load_json("ambulancias")
    nuevo_id = max([a["id"] for a in ambulancias], default=0) + 1
    amb["id"] = nuevo_id
    ambulancias.append(amb)
    save_json("ambulancias", ambulancias)
    return amb

@router.put("/{amb_id}")
def modificar_ambulancia(amb_id: int, cambios: dict[str, object]):
    ambulancias = load_json("ambulancias")
    amb = find_by_id(ambulancias, amb_id)
    if not amb:
        raise HTTPException(404, "Ambulancia no encontrada")
    amb.update(cambios)
    save_json("ambulancias", ambulancias)
    return amb
