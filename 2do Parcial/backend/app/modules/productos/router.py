from typing import Annotated

from app.core.database import SessionDep
from app.modules.productos.schema import (
    CategoriaProductoPublic,
    ClasificacionCreate,
    ClasificacionPublic,
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)
from app.modules.productos.service import (
    actualizar_producto,
    clasificar_producto,
    crear_producto,
    desactivar_producto,
    listar_categorias_producto,
    listar_productos,
    obtener_producto_por_id,
)
from fastapi import APIRouter, Path, Query, status

router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])



@router.post("/", response_model=ProductoPublic, status_code=status.HTTP_201_CREATED)
def alta_producto(producto: ProductoCreate, session: SessionDep):
    return crear_producto(session, producto)

@router.get("/", response_model=list[ProductoPublic], status_code=status.HTTP_200_OK)
def obtener_productos(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    activo: bool | None = None, # Por defecto trae solo activos
    disponible: bool | None = None,
    categoria_id: int | None = None,
    search: str | None = None,
):
    return listar_productos(session, skip, limit, activo, disponible, categoria_id, search)

@router.get("/{id}", response_model=ProductoPublic, status_code=status.HTTP_200_OK)
def obtener(
    session: SessionDep,
    id: int = Path(..., gt=0),
):
    producto = obtener_producto_por_id(
        session=session,
        producto_id=id,
    )

    return ProductoPublic(
        **producto.model_dump(),
        unidad_venta=producto.unidad_venta,
        categorias=producto.categorias,
        hay_stock=producto.stock_cantidad > 0,
    )

@router.put("/{id}", response_model=ProductoPublic, status_code=status.HTTP_200_OK)
def actualizar(
    data: ProductoUpdate,
    session: SessionDep,
    id: int = Path(..., gt=0),
):
    return actualizar_producto(session=session, producto_id=id, data=data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar(
    session: SessionDep,
    id: int = Path(..., gt=0),
):
    desactivar_producto(session=session, producto_id=id)
    
# --- Endpoints de Relaciones N:N ---

@router.post("/{id}/categorias", response_model=ClasificacionPublic, status_code=status.HTTP_201_CREATED)
def clasificar(
    data: ClasificacionCreate,
    session: SessionDep,
    id: int = Path(..., gt=0),
):
    return clasificar_producto(
        session=session,
        producto_id=id,
        categoria_id=data.categoria_id,
        es_principal=data.es_principal,
    )

@router.get("/{id}/categorias", response_model=list[CategoriaProductoPublic], status_code=status.HTTP_200_OK)
def listar_categorias(
    session: SessionDep,
    id: int = Path(..., gt=0),
):
    return listar_categorias_producto(session=session, producto_id=id)