from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

# Coincide con OpenAPI: /v1/control_insumos
router = APIRouter(prefix="/v1/control_insumos")


@router.get("")
def listar_controles():
    return load_json("control_insumos")


@router.get("/{control_id}")
def obtener_control(control_id: int):
    controles = load_json("control_insumos")
    control = find_by_id(controles, control_id)
    if not control:
        raise HTTPException(404, "Control no encontrado")
    return control


@router.post("")
def crear_control(body: dict):
    """
    Body según OpenAPI (ControlInsumoRequestDTO):
    {
      "id": 1,
      "cantidad": 10,
      "cantidadRestockeo": 0
    }
    """
    controles = load_json("control_insumos")
    nuevo_id = max([c["id"] for c in controles], default=0) + 1

    nuevo_control = {
        "id": nuevo_id,
        "turno_id": body["turnoId"],
        "insumo_id": body["insumoId"],
        "cantidad_ingreso": body.get("cantidadIngreso"),
        "cantidad_restockeo": body.get("cantidadRestockeo", 0),
        "cantidad_egreso": body.get("cantidadEgreso")
    }

    controles.append(nuevo_control)
    save_json("control_insumos", controles)
    return nuevo_control


@router.put("/{control_id}")
def modificar_control(control_id: int, body: dict):
    controles = load_json("control_insumos")
    control = find_by_id(controles, control_id)

    if not control:
        raise HTTPException(404, "Control no encontrado")

    if "cantidadIngreso" in body:
        control["cantidad_ingreso"] = body["cantidadIngreso"]

    if "cantidadRestockeo" in body:
        control["cantidad_restockeo"] = body["cantidadRestockeo"]

    if "cantidadEgreso" in body:
        control["cantidad_egreso"] = body["cantidadEgreso"]

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
    return {"status": "OK", "id": control_id}
