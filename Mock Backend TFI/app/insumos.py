from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

router = APIRouter(prefix="/insumos")

@router.get("")
def get_insumos():
    return load_json("insumos")

@router.post("")
def crear_insumo(insumo: dict[str, object]):
    insumos = load_json("insumos")
    nuevo_id = max([i["id"] for i in insumos], default=0) + 1
    insumo["id"] = nuevo_id
    insumos.append(insumo)
    save_json("insumos", insumos)
    return insumo

@router.put("/{insumo_id}")
def modificar_insumo(insumo_id: int, cambios: dict[str, object]):
    insumos = load_json("insumos")
    insumo = find_by_id(insumos, insumo_id)
    if not insumo:
        raise HTTPException(404, "Insumo no encontrado")
    insumo.update(cambios)
    save_json("insumos", insumos)
    return insumo
