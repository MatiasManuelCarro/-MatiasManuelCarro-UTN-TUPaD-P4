from fastapi import APIRouter, HTTPException, Path, Query, status

from database import SessionDep

from ..schemas import categoria
from ..service import categoria_services

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.post(
    "/", response_model=categoria.CategoriaPublic, status_code=status.HTTP_201_CREATED
)
def alta_categoria(categoria: categoria.CategoriaCreate, session: SessionDep):
    return categoria_services.crear(session, categoria)


@router.get(
    "/", response_model=list[categoria.CategoriaPublic], status_code=status.HTTP_200_OK
)
def listar_categorias(
    session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(10, le=50)
):
    return categoria_services.obtener_todas(session, skip, limit)


@router.get(
    "/{id}", response_model=categoria.CategoriaPublic, status_code=status.HTTP_200_OK
)
def detalle_categoria(session: SessionDep, id: int = Path(..., gt=0)):
    categoria = categoria_services.obtener_por_id(session, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )
    return categoria


@router.put(
    "/{id}", response_model=categoria.CategoriaPublic, status_code=status.HTTP_200_OK
)
def actualizar_categoria(
    *, #soluciona el problema del orden dentro de los parametros
    session: SessionDep,
    data: categoria.CategoriaUpdate,
    id: int = Path(...),
):
    actualizada = categoria_services.actualizar_total(session, data, id)
    if not actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return actualizada



@router.put(
    "/{id}/desactivar",
    response_model=categoria.CategoriaPublic,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(session: SessionDep, id: int = Path(..., gt=0)):
    desactivada = categoria_services.desactivar(session, id)
    if not desactivada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
        )
    return desactivada
