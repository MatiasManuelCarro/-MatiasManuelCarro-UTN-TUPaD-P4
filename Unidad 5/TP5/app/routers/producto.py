from fastapi import APIRouter, HTTPException, Path, Query, status

from ..service import producto_services
from ..schemas import producto

router = APIRouter(prefix="/productos", tags=["Productos"])


# ---------------------------------------------------------
# ALTA DE PRODUCTO
# Método: POST | Endpoint: /productos | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/", response_model=producto.ProductoRead, status_code=status.HTTP_201_CREATED
)
def alta_producto(producto: producto.ProductoCreate):
    return producto_services.crear(producto)


# (Extra) LISTAR PRODUCTOS
@router.get(
    "/", response_model=list[producto.ProductoRead], status_code=status.HTTP_200_OK
)
def listar_productos(skip: int = Query(0, ge=0), limit: int = Query(10, le=50)):
    return producto_services.obtener_todos(skip, limit)


# ---------------------------------------------------------
# DETALLE DE PRODUCTO
# Método: GET | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}", response_model=producto.ProductoRead, status_code=status.HTTP_200_OK
)
def detalle_producto(id: int = Path(..., gt=0)):
    producto = producto_services.obtener_por_id(id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto


# ---------------------------------------------------------
# ACTUALIZACIÓN (Reemplazo Total)
# Método: PUT | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}", response_model=producto.ProductoRead, status_code=status.HTTP_200_OK
)
def actualizar_producto(producto: producto.ProductoCreate, id: int = Path(..., gt=0)):
    # Usamos ProductoCreate porque es un reemplazo total (exige todos los campos)
    actualizado = producto_services.actualizar_total(id, producto)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return actualizado


# ---------------------------------------------------------
# BORRADO LÓGICO
# Método: PUT | Endpoint: /productos/{id}/desactivar | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}/desactivar",
    response_model=producto.ProductoRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivado = producto_services.desactivar(id)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return desactivado


# ---------------------------------------------------------
# CONSULTAR STOCK (Lógica de Negocio)
# Método: GET | Endpoint: /productos/{id}/stock | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}/stock",
    response_model=producto.ProductoStockResponse,
    status_code=status.HTTP_200_OK,
)
@router.get("/{id}/stock", response_model=producto.ProductoStockResponse)
def consultar_stock(id: int = Path(..., gt=0)):
    resultado = producto_services.obtener_estado_stock(id)  # Llamada al servicio
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return resultado  # El router solo devuelve el resultado
