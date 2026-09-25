from fastapi import APIRouter, HTTPException, Path, Query, status

from . import schemas, services

router = APIRouter(prefix="/proveedores", tags=["proveedores"])


# ---------------------------------------------------------
# ALTA DE PROVEEDOR
# Método: POST | Endpoint: /proveedores | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/", response_model=schemas.ProveedorRead, status_code=status.HTTP_201_CREATED
)
def alta_proveedor(proveedor: schemas.ProveedorCreate):
    return services.crear(proveedor)

# ---------------------------------------------------------
# OBTENER PROVEEDORES (Todos / Activos / Inactivos)
# Método: GET | Endpoint: /proveedores | Estado: 200 OK
# Activos / inactivos:
# GET /proveedores/?activo=true
# GET /proveedores/?activo=false
# ---------------------------------------------------------
@router.get(
    "/", response_model=list[schemas.ProveedorRead], status_code=status.HTTP_200_OK
)
def listar_proveedores(
    activo: bool | None = Query(None, description="Filtra por estado (True=activos, False=inactivos, ausente=todos)"),
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, le=50)
):
    return services.obtener_proveedores(activo, skip, limit)


# ---------------------------------------------------------
# DETALLE DE PROVEEDOR
# Método: GET | Endpoint: /proveedores/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def detalle_proveedor(id: int = Path(..., gt=0)):
    proveedor = services.obtener_por_id(id)
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    return proveedor

# ---------------------------------------------------------
# ACTUALIZACIÓN (Reemplazo Total)
# Método: PUT | Endpoint: /proveedores/{id} | Estado: 200 OK
# ---------------------------------------------------------

@router.put(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def actualizar_proveedor(proveedor: schemas.ProveedorCreate, id: int = Path(..., gt=0)):
    # Usamos ProductoCreate porque es un reemplazo total (exige todos los campos)
    actualizado = services.actualizar_total(id, proveedor)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    return actualizado


# ---------------------------------------------------------
# BORRADO LÓGICO
# Método: PUT | Endpoint: /proveedores/{id}/desactivar | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    return desactivado
