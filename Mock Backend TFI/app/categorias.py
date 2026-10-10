from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

router = APIRouter(prefix="/categorias")


@router.get("")
def get_categorias():
    return load_json("categorias")


@router.post("")
def crear_categoria(categoria: dict[str, object]):
    categorias = load_json("categorias")
    nuevo_id = max([c["id"] for c in categorias], default=0) + 1
    categoria["id"] = nuevo_id
    categorias.append(categoria)
    save_json("categorias", categorias)
    return categoria


@router.put("/{categoria_id}")
def modificar_categoria(categoria_id: int, cambios: dict[str, object]):
    categorias = load_json("categorias")
    categoria = find_by_id(categorias, categoria_id)
    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")
    categoria.update(cambios)
    save_json("categorias", categorias)
    return categoria


@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    categorias = load_json("categorias")
    categoria = find_by_id(categorias, categoria_id)
    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")
    categoria["activo"] = False
    save_json("categorias", categorias)
    return {"mensaje": "Categoría desactivada", "id": categoria_id}
