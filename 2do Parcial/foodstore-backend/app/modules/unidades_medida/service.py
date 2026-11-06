from app.modules.productos.schema import UnidadMedidaPublic
from app.modules.unidades_medida.model import UnidadMedida
from sqlmodel import Session, select


def listar_unidades(session: Session) -> list[UnidadMedidaPublic]:
    unidades = session.exec(
        select(UnidadMedida)
    ).all()

    return [
        UnidadMedidaPublic(**unidad.model_dump())
        for unidad in unidades
    ]