from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

# Coincide con OpenAPI: /v1/insumos
router = APIRouter(prefix="/v1/insumos")


@router.get("")
def listar_insumos():
    # Responde array de InsumoDTO
    return load_json("insumos")


@router.get("/{insumo_id}")
def obtener_insumo(insumo_id: int):
    insumos = load_json("insumos")
    insumo = find_by_id(insumos, insumo_id)
    if not insumo:
        raise HTTPException(404, "Insumo no encontrado")
    return insumo


@router.post("")
def crear_insumo(body: dict):
    """
    Body según OpenAPI (InsumoRequestDTO):
    {
      "nombre": "Gasas",
      "categoriaId": 3,
      "puntoControl": 10,
      "critico": false
    }
    """
    insumos = load_json("insumos")
    nuevo_id = max([i["id"] for i in insumos], default=0) + 1

    nuevo_insumo = {
      "id": nuevo_id,
      "nombre": body["nombre"],
      # En el mock guardamos categoriaId y categoria (string) opcional
      "categoriaId": body["categoriaId"],
      "categoria": body.get("categoria"),  # si querés después lo resolvés por ID
      "puntoControl": body["puntoControl"],
      "esCritico": body["critico"]
    }

    insumos.append(nuevo_insumo)
    save_json("insumos", insumos)
    return nuevo_insumo


@router.put("/{insumo_id}")
def modificar_insumo(insumo_id: int, body: dict):
    """
    Body según OpenAPI (InsumoRequestDTO):
    campos opcionales:
    - nombre
    - categoriaId
    - puntoControl
    - critico
    """
    insumos = load_json("insumos")
    insumo = find_by_id(insumos, insumo_id)

    if not insumo:
        raise HTTPException(404, "Insumo no encontrado")

    if "nombre" in body:
        insumo["nombre"] = body["nombre"]
    if "categoriaId" in body:
        insumo["categoriaId"] = body["categoriaId"]
    if "puntoControl" in body:
        insumo["puntoControl"] = body["puntoControl"]
    if "critico" in body:
        insumo["esCritico"] = body["critico"]

    save_json("insumos", insumos)
    return insumo


@router.delete("/{insumo_id}")
def eliminar_insumo(insumo_id: int):
    insumos = load_json("insumos")
    insumo = find_by_id(insumos, insumo_id)
    if not insumo:
        raise HTTPException(404, "Insumo no encontrado")

    insumos = [i for i in insumos if i["id"] != insumo_id]
    save_json("insumos", insumos)
    return {"status": "OK", "id": insumo_id}
