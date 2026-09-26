# app/routers/categoria.py

from fastapi import APIRouter, HTTPException, Path, Query, status
from app.database import SessionDep

from app.schemas.categoria import CategoriaCreate, CategoriaPublic, CategoriaUpdate
from app.service.categoria_services import (
    crear_categoria,
    listar_categorias,
    obtener_categoria_por_id,
    actualizar_categoria,
    desactivar_categoria,
)

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.post("/", response_model=CategoriaPublic, status_code=status.HTTP_201_CREATED)
def alta_categoria(categoria: CategoriaCreate, session: SessionDep):
    return crear_categoria(session, categoria)


@router.get("/", response_model=list[CategoriaPublic], status_code=status.HTTP_200_OK)
def obtener_categorias(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    activo: bool | None = None,
):
    return listar_categorias(session, skip, limit, activo)


@router.get("/{categoria_id}", response_model=CategoriaPublic, status_code=status.HTTP_200_OK)
def detalle_categoria(session: SessionDep, categoria_id: int = Path(..., gt=0)):
    return obtener_categoria_por_id(session, categoria_id)

@router.patch("/{categoria_id}", response_model=CategoriaPublic, status_code=status.HTTP_200_OK)
def modificar_categoria(
    categoria_id: int = Path(..., gt=0),
    data: CategoriaUpdate = None,
    session: SessionDep = None,
):
    return actualizar_categoria(session, categoria_id, data)


@router.patch("/{categoria_id}/desactivar", response_model=CategoriaPublic, status_code=status.HTTP_200_OK)
def desactivar_categoria_endpoint(categoria_id: int = Path(..., gt=0), session: SessionDep = None):
    return desactivar_categoria(session, categoria_id)
