from app.categoria.schema import (
    CategoriaCreate,
    CategoriaPaginatedResponse,
    CategoriaPublic,
    CategoriaUpdate,
)
from app.categoria.service import (
    actualizar_categoria,
    crear_categoria,
    eliminar_categoria,
    listar_categorias,
    obtener_categoria_por_id,
)
from app.core.database import SessionDep
from fastapi import APIRouter, Path, Query, status

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.post("/", response_model=CategoriaPublic, status_code=status.HTTP_201_CREATED)
def alta_categoria(data: CategoriaCreate, session: SessionDep):
    return crear_categoria(session, data)


@router.get("/", response_model=CategoriaPaginatedResponse)
def obtener_categorias(
    session: SessionDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    nombre: str | None = Query(None),
    incluir_inactivos: bool = Query(False),
):
    return listar_categorias(session, offset, limit, nombre, incluir_inactivos)



@router.get("/{categoria_id}", response_model=CategoriaPublic)
def detalle_categoria(session: SessionDep, categoria_id: int = Path(..., gt=0)):
    return obtener_categoria_por_id(session, categoria_id)


@router.get("/{categoria_id}/productos", response_model=list[int])
def productos_de_categoria(session: SessionDep, categoria_id: int = Path(..., gt=0)):
    categoria = obtener_categoria_por_id(session, categoria_id)
    return [p.id for p in categoria.productos]


@router.put("/{categoria_id}", response_model=CategoriaPublic)
def modificar_categoria(
    categoria_id: int = Path(..., gt=0),
    data: CategoriaUpdate = None,
    session: SessionDep = None,
):
    return actualizar_categoria(session, categoria_id, data)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria_endpoint(session: SessionDep, categoria_id: int = Path(..., gt=0)):
    eliminar_categoria(session, categoria_id)
