from app.core.database import SessionDep
from app.producto_categoria.schema import (
    ProductoCategoriaCreate,
    ProductoCategoriaPublic,
)
from app.producto_categoria.service import (
    crear_relacion,
    eliminar_relacion,
    listar_relaciones,
)
from fastapi import APIRouter, Path, status

router = APIRouter(prefix="/producto-categoria", tags=["ProductoCategoria"])


@router.post("/", response_model=ProductoCategoriaPublic, status_code=status.HTTP_201_CREATED)
def alta_relacion(data: ProductoCategoriaCreate, session: SessionDep):
    return crear_relacion(session, data)


@router.get("/", response_model=list[ProductoCategoriaPublic])
def obtener_relaciones(session: SessionDep):
    return listar_relaciones(session)


@router.delete("/{producto_id}/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_relacion_endpoint(
    producto_id: int = Path(..., gt=0),
    categoria_id: int = Path(..., gt=0),
    session: SessionDep = None,
):
    eliminar_relacion(session, producto_id, categoria_id)
