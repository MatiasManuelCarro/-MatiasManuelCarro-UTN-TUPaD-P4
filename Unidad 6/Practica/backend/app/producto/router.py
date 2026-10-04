from fastapi import APIRouter, Path, Query, status

from app.core.database import SessionDep
from app.producto.schema import (
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)
from app.producto.service import (
    actualizar_producto,
    crear_producto,
    desactivar_producto,
    eliminar_producto,
    listar_productos,
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

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto_endpoint(producto_id: int = Path(..., gt=0), session: SessionDep = None):
    eliminar_producto(session, producto_id)
