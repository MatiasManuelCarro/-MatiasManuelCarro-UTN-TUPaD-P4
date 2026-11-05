from app.core.database import SessionDep
from app.modules.categorias.schema import (
    CategoriaCreate,
    CategoriaPublic,
    CategoriaUpdate,
)
from app.modules.categorias.service import (
    actualizar_categoria,
    crear_categorias,
    desactivar_categoria,
    listar_categorias,
    obtener_categorias_por_id,
)
from fastapi import APIRouter, Path, status

router = APIRouter(prefix="/api/v1/categorias", tags=["Categorias"])


# * POST /api/v1/categorias
@router.post("/", response_model=CategoriaPublic, status_code=status.HTTP_201_CREATED)
def crear(data: CategoriaCreate, session: SessionDep):
    return crear_categorias(session, data)


# * GET /api/v1/categorias
@router.get("/", response_model=list[CategoriaPublic], status_code=status.HTTP_200_OK)
def listar(session: SessionDep, activo: bool | None = None, search: str | None = None):
    return listar_categorias(session=session, activo=activo, search=search)


# * GET /api/v1/categorias/{id}
@router.get("/{id}", response_model=CategoriaPublic, status_code=status.HTTP_200_OK)
def obtener(session: SessionDep, id: int = Path(..., gt=0)):
    categoria = obtener_categorias_por_id(session=session, categoria_id=id)

    return CategoriaPublic(**categoria.model_dump())


# * PUT /api/v1/categorias/{id}
@router.put("/{id}", response_model=CategoriaPublic, status_code=status.HTTP_200_OK)
def actualizar(data: CategoriaUpdate, session: SessionDep, id: int = Path(..., gt=0)):
    return actualizar_categoria(session=session, categoria_id=id, data=data)


# * DELETE /api/v1/categorias/{id}
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar(session: SessionDep, id: int = Path(..., gt=0)):
    desactivar_categoria(session=session, categoria_id=id)
