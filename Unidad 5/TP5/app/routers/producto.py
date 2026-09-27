from fastapi import APIRouter, Path, Query, status

from app.database import SessionDep
from app.schemas.producto import (
    ProductoCreate,
    ProductoPublic,
    ProductoStockResponse,
    ProductoUpdate,
)
from app.service.producto_services import (
    actualizar_producto,
    crear_producto,
    desactivar_producto,
    listar_productos,
    obtener_estado_stock,
    obtener_producto_por_id,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoPublic, status_code=status.HTTP_201_CREATED)
def alta_producto(producto: ProductoCreate, session: SessionDep):
    return crear_producto(session, producto)


@router.get("/", response_model=list[ProductoPublic], status_code=status.HTTP_200_OK)
def obtener_productos(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    activo: bool | None = None,
):
    return listar_productos(session, skip, limit, activo)


@router.get("/{producto_id}", response_model=ProductoPublic, status_code=status.HTTP_200_OK)
def detalle_producto(session: SessionDep, producto_id: int = Path(..., gt=0)):
    return obtener_producto_por_id(session, producto_id)


@router.patch("/{producto_id}", response_model=ProductoPublic, status_code=status.HTTP_200_OK)
def modificar_producto(
    producto_id: int = Path(..., gt=0),
    data: ProductoUpdate = None,
    session: SessionDep = None,
):
    return actualizar_producto(session, producto_id, data)


@router.patch("/{producto_id}/desactivar", response_model=ProductoPublic, status_code=status.HTTP_200_OK)
def desactivar_producto_endpoint(producto_id: int = Path(..., gt=0), session: SessionDep = None):
    return desactivar_producto(session, producto_id)


@router.get("/{producto_id}/stock", response_model=ProductoStockResponse, status_code=status.HTTP_200_OK)
def consultar_stock(session: SessionDep, producto_id: int = Path(..., gt=0)):
    return obtener_estado_stock(session, producto_id)
