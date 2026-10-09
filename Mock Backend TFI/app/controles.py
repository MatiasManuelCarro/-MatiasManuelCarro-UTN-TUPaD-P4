from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

router = APIRouter(prefix="/control_insumos")

@router.post("")
def crear_control(control: dict[str, object]):
    controles = load_json("control_insumos")
    nuevo_id = max([c["id"] for c in controles], default=0) + 1
    control["id"] = nuevo_id
    controles.append(control)
    save_json("control_insumos", controles)
    return control

@router.put("/{control_id}")
def modificar_control(control_id: int, cambios: dict[str, object]):
    controles = load_json("control_insumos")
    control = find_by_id(controles, control_id)
    if not control:
        raise HTTPException(404, "Control no encontrado")
    control.update(cambios)
    save_json("control_insumos", controles)
    return control

@router.delete("/{control_id}")
def eliminar_control(control_id: int):
    controles = load_json("control_insumos")
    control = find_by_id(controles, control_id)
    if not control:
        raise HTTPException(404, "Control no encontrado")
    controles = [c for c in controles if c["id"] != control_id]
    save_json("control_insumos", controles)
    return {"mensaje": "Control eliminado", "id": control_id}
