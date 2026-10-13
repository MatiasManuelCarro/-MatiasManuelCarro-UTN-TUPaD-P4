from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

# Coincide con OpenAPI: /v1/ambulancias
router = APIRouter(prefix="/v1/ambulancias")


@router.get("")
def listar_ambulancias():
    return load_json("ambulancias")


@router.get("/{amb_id}")
def obtener_ambulancia(amb_id: int):
    ambulancias = load_json("ambulancias")
    amb = find_by_id(ambulancias, amb_id)
    if not amb:
        raise HTTPException(404, "Ambulancia no encontrada")
    return amb


@router.post("")
def crear_ambulancia(body: dict):
    """
    Body según OpenAPI (AmbulanciaRequestDTO):
    {
      "patente": "AA123BB",
      "disponible": true,
      "insumos": [1,2,3]
    }
    """
    ambulancias = load_json("ambulancias")
    nuevo_id = max([a["id"] for a in ambulancias], default=0) + 1

    nueva = {
        "id": nuevo_id,
        "patente": body["patente"],
        # El OpenAPI incluye disponible e insumos, pero el DTO de respuesta solo devuelve id + patente
        "disponible": body.get("disponible", True),
        "insumos": body.get("insumos", [])
    }

    ambulancias.append(nueva)
    save_json("ambulancias", ambulancias)
    return nueva


@router.put("/{amb_id}")
def modificar_ambulancia(amb_id: int, body: dict):
    ambulancias = load_json("ambulancias")
    amb = find_by_id(ambulancias, amb_id)

    if not amb:
        raise HTTPException(404, "Ambulancia no encontrada")

    if "patente" in body:
        amb["patente"] = body["patente"]
    if "disponible" in body:
        amb["disponible"] = body["disponible"]
    if "insumos" in body:
        amb["insumos"] = body["insumos"]

    save_json("ambulancias", ambulancias)
    return amb


@router.delete("/{amb_id}")
def eliminar_ambulancia(amb_id: int):
    ambulancias = load_json("ambulancias")
    amb = find_by_id(ambulancias, amb_id)

    if not amb:
        raise HTTPException(404, "Ambulancia no encontrada")

    ambulancias = [a for a in ambulancias if a["id"] != amb_id]
    save_json("ambulancias", ambulancias)
    return {"status": "OK", "id": amb_id}
