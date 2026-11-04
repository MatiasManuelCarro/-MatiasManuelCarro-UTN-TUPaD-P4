from app.core.database import SessionDep
from app.modules.productos.schema import UnidadMedidaPublic
from app.modules.unidades_medida.model import UnidadMedida
from fastapi import APIRouter, status
from sqlmodel import select

router = APIRouter(
    prefix="/api/v1/unidades-medida",
    tags=["Unidades de medida"],
)


@router.get(
    "/",
    response_model=list[UnidadMedidaPublic],
    status_code=status.HTTP_200_OK,
)
def listar_unidades(session: SessionDep):
    unidades = session.exec(select(UnidadMedida)).all()

    return [UnidadMedidaPublic(**unidad.model_dump()) for unidad in unidades]
