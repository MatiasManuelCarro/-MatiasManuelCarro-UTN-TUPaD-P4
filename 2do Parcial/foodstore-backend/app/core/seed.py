from sqlmodel import Session, select

from app.core.database import engine
from app.modules.unidades_medida.model import TipoUnidad, UnidadMedida


def seed_unidades_medida():
    with Session(engine) as session:

        # verificacion si ya existen unidades
        unidad_existente = session.exec(
            select(UnidadMedida)
        ).first()

        if unidad_existente:
            return

        unidades = [
            UnidadMedida(
                nombre="kilogramo",
                simbolo="kg",
                tipo=TipoUnidad.PESO,
            ),
            UnidadMedida(
                nombre="gramo",
                simbolo="g",
                tipo=TipoUnidad.PESO,
            ),
            UnidadMedida(
                nombre="litro",
                simbolo="L",
                tipo=TipoUnidad.VOLUMEN,
            ),
            UnidadMedida(
                nombre="mililitro",
                simbolo="mL",
                tipo=TipoUnidad.VOLUMEN,
            ),
            UnidadMedida(
                nombre="pieza",
                simbolo="u",
                tipo=TipoUnidad.CONTABLE,
            ),
            UnidadMedida(
                nombre="docena",
                simbolo="doc",
                tipo=TipoUnidad.CONTABLE,
            ),
        ]

        session.add_all(unidades)
        session.commit()