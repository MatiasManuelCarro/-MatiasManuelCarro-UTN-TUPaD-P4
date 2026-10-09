from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

router = APIRouter(prefix="/usuarios")

@router.get("")
def get_usuarios():
    return load_json("usuarios")

@router.post("")
def crear_usuario(usuario: dict[str, object]):
    usuarios = load_json("usuarios")
    nuevo_id = max([u["id"] for u in usuarios], default=0) + 1
    usuario["id"] = nuevo_id
    usuarios.append(usuario)
    save_json("usuarios", usuarios)
    return usuario

@router.put("/{usuario_id}")
def modificar_usuario(usuario_id: int, cambios: dict[str, object]):
    usuarios = load_json("usuarios")
    usuario = find_by_id(usuarios, usuario_id)
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")
    usuario.update(cambios)
    save_json("usuarios", usuarios)
    return usuario

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    usuarios = load_json("usuarios")
    usuario = find_by_id(usuarios, usuario_id)
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")
    usuario["activo"] = False
    save_json("usuarios", usuarios)
    return {"mensaje": "Usuario desactivado", "id": usuario_id}
