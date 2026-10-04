from fastapi import APIRouter, Path, Query, status

from app.categoria.schema import CategoriaCreate, CategoriaPublic, CategoriaUpdate
from app.categoria.service import (
    actualizar_categoria,
    crear_categoria,
    eliminar_categoria,
    listar_categorias,
    obtener_categoria_por_id,
)
from app.core.database import SessionDep

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.post("/", response_model=CategoriaPublic, status_code=status.HTTP_201_CREATED)
def alta_categoria(categoria: CategoriaCreate, session: SessionDep):
    return crear_categoria(session, categoria)


@router.get("/", response_model=list[CategoriaPublic], status_code=status.HTTP_200_OK)
def obtener_categorias(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
):
    return listar_categorias(session, skip, limit)


@router.get(
    "/{categoria_id}", response_model=CategoriaPublic, status_code=status.HTTP_200_OK
)
def detalle_categoria(session: SessionDep, categoria_id: int = Path(..., gt=0)):
    return obtener_categoria_por_id(session, categoria_id)


@router.patch(
    "/{categoria_id}", response_model=CategoriaPublic, status_code=status.HTTP_200_OK
)
def modificar_categoria(
    categoria_id: int = Path(..., gt=0),
    data: CategoriaUpdate = None,
    session: SessionDep = None,
):
    return actualizar_categoria(session, categoria_id, data)

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria_endpoint(session: SessionDep, categoria_id: int = Path(..., gt=0)):
    eliminar_categoria(session, categoria_id)


