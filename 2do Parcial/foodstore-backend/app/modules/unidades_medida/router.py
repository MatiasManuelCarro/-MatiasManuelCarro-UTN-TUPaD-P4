from app.core.database import SessionDep
from app.modules.productos.schema import UnidadMedidaPublic
from app.modules.unidades_medida.service import listar_unidades
from fastapi import APIRouter, status

router = APIRouter(
    prefix="/api/v1/unidades-medida",
    tags=["Unidades de medida"],
)


@router.get(
    "/",
    response_model=list[UnidadMedidaPublic],
    status_code=status.HTTP_200_OK,
)
def listar(session: SessionDep):
    return listar_unidades(session)