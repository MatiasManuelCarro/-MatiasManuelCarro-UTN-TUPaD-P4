from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

# Coincide con OpenAPI: /v1/categorias
router = APIRouter(prefix="/v1/categorias")


@router.get("")
def listar_categorias():
    return load_json("categorias")


@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    categorias = load_json("categorias")
    categoria = find_by_id(categorias, categoria_id)
    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")
    return categoria


@router.post("")
def crear_categoria(body: dict):
    """
    Body según OpenAPI (CategoriaInsumoRequestDTO):
    {
      "nombre": "Medicamentos",
      "color": "#FF5555"
    }
    """
    categorias = load_json("categorias")
    nuevo_id = max([c["id"] for c in categorias], default=0) + 1

    nueva_categoria = {
        "id": nuevo_id,
        "nombre": body["nombre"],
        "color": body["color"]
    }

    categorias.append(nueva_categoria)
    save_json("categorias", categorias)
    return nueva_categoria


@router.put("/{categoria_id}")
def modificar_categoria(categoria_id: int, body: dict):
    categorias = load_json("categorias")
    categoria = find_by_id(categorias, categoria_id)

    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")

    if "nombre" in body:
        categoria["nombre"] = body["nombre"]
    if "color" in body:
        categoria["color"] = body["color"]

    save_json("categorias", categorias)
    return categoria


@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    categorias = load_json("categorias")
    categoria = find_by_id(categorias, categoria_id)

    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")

    categorias = [c for c in categorias if c["id"] != categoria_id]
    save_json("categorias", categorias)
    return {"status": "OK", "id": categoria_id}
