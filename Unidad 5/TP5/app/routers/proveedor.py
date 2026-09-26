from fastapi import APIRouter, Path, Query, status

from app.database import SessionDep
from app.schemas.proveedor import ProveedorCreate, ProveedorPublic, ProveedorUpdate
from app.service.proveedor_services import (
    actualizar_proveedor,
    crear_proveedor,
    desactivar_proveedor,
    listar_proveedores,
    obtener_proveedor_por_id,
)

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.post("/", response_model=ProveedorPublic, status_code=status.HTTP_201_CREATED)
def alta_proveedor(proveedor: ProveedorCreate, session: SessionDep):
    return crear_proveedor(session, proveedor)


@router.get("/", response_model=list[ProveedorPublic], status_code=status.HTTP_200_OK)
def obtener_proveedores(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    activo: bool | None = None,
):
    return listar_proveedores(session, skip, limit, activo)


@router.get("/{proveedor_id}", response_model=ProveedorPublic, status_code=status.HTTP_200_OK)
def detalle_proveedor(session: SessionDep, proveedor_id: int = Path(..., gt=0)):
    return obtener_proveedor_por_id(session, proveedor_id)


@router.patch("/{proveedor_id}", response_model=ProveedorPublic, status_code=status.HTTP_200_OK)
def modificar_proveedor(
    proveedor_id: int = Path(..., gt=0),
    data: ProveedorUpdate = None,
    session: SessionDep = None,
):
    return actualizar_proveedor(session, proveedor_id, data)


@router.patch("/{proveedor_id}/desactivar", response_model=ProveedorPublic, status_code=status.HTTP_200_OK)
def desactivar_proveedor_endpoint(proveedor_id: int = Path(..., gt=0), session: SessionDep = None):
    return desactivar_proveedor(session, proveedor_id)
