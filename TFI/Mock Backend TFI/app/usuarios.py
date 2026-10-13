from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

# Coincide con OpenAPI: /v1/usuarios
router = APIRouter(prefix="/v1/usuarios")


@router.get("")
def listar_usuarios():
    return load_json("usuarios")


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    usuarios = load_json("usuarios")
    usuario = find_by_id(usuarios, usuario_id)
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")
    return usuario


@router.post("")
def crear_usuario(body: dict):
    """
    Body según OpenAPI (UsuarioRequestDTO):
    {
      "nombre": "string",
      "dni": "string",
      "email": "string",
      "rol": "ADMINISTRADOR" | "ENFERMERO",
      "clave": "string",
      "activo": true
    }
    """
    usuarios = load_json("usuarios")
    nuevo_id = max([u["id"] for u in usuarios], default=0) + 1

    nuevo_usuario = {
        "id": nuevo_id,
        "nombre": body["nombre"],
        "dni": body.get("dni"),
        "email": body["email"],
        "rol": body["rol"],
        "activo": body.get("activo", True)
    }

    usuarios.append(nuevo_usuario)
    save_json("usuarios", usuarios)
    return nuevo_usuario


@router.put("/{usuario_id}")
def modificar_usuario(usuario_id: int, body: dict):
    usuarios = load_json("usuarios")
    usuario = find_by_id(usuarios, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    for campo in ["nombre", "dni", "email", "rol", "activo"]:
        if campo in body:
            usuario[campo] = body[campo]

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
    return {"status": "OK", "id": usuario_id}
