from decimal import Decimal

from sqlmodel import Session, select

from app.core.database import engine
from app.modules.productos.model import Producto
from app.modules.unidades_medida.model import TipoUnidad, UnidadMedida


def seed_unidades_medida():
    with Session(engine) as session:

        # verificacion de unidades existentes
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

def seed_productos():
    with Session(engine) as session:

        producto_existente = session.exec(
            select(Producto)
        ).first()

        if producto_existente:
            return

        unidades = session.exec(
            select(UnidadMedida)
        ).all()

        unidad_por_nombre = {
            unidad.nombre: unidad
            for unidad in unidades
        }

        productos = [
            # Kilogramo
            Producto(
                nombre="Harina integral",
                descripcion="Harina integral a granel",
                precio_base=Decimal("1850.50"),
                unidad_venta_id=unidad_por_nombre["kilogramo"].id,
                stock_cantidad=Decimal("24.750"),
                disponible=True,
            ),
            Producto(
                nombre="Queso cremoso",
                descripcion="Queso cremoso por kilogramo",
                precio_base=Decimal("9200.00"),
                unidad_venta_id=unidad_por_nombre["kilogramo"].id,
                stock_cantidad=Decimal("12.500"),
                disponible=True,
            ),

            # Gramo
            Producto(
                nombre="Nueces",
                descripcion="Nueces por gramo",
                precio_base=Decimal("8.50"),
                unidad_venta_id=unidad_por_nombre["gramo"].id,
                stock_cantidad=Decimal("850.000"),
                disponible=True,
            ),
            Producto(
                nombre="Chocolate",
                descripcion="Chocolate por gramo",
                precio_base=Decimal("12.00"),
                unidad_venta_id=unidad_por_nombre["gramo"].id,
                stock_cantidad=Decimal("650.000"),
                disponible=True,
            ),

            # Litro
            Producto(
                nombre="Aceite de oliva",
                descripcion="Aceite de oliva por litro",
                precio_base=Decimal("7200.00"),
                unidad_venta_id=unidad_por_nombre["litro"].id,
                stock_cantidad=Decimal("18.500"),
                disponible=True,
            ),
            Producto(
                nombre="Jugo de naranja",
                descripcion="Jugo de naranja por litro",
                precio_base=Decimal("2800.00"),
                unidad_venta_id=unidad_por_nombre["litro"].id,
                stock_cantidad=Decimal("14.250"),
                disponible=True,
            ),

            # Mililitro
            Producto(
                nombre="Salsa picante",
                descripcion="Salsa picante por mililitro",
                precio_base=Decimal("5.50"),
                unidad_venta_id=unidad_por_nombre["mililitro"].id,
                stock_cantidad=Decimal("750.000"),
                disponible=True,
            ),
            Producto(
                nombre="Esencia de vainilla",
                descripcion="Esencia de vainilla por mililitro",
                precio_base=Decimal("7.00"),
                unidad_venta_id=unidad_por_nombre["mililitro"].id,
                stock_cantidad=Decimal("420.000"),
                disponible=True,
            ),

            # Pieza
            Producto(
                nombre="Alfajor",
                descripcion="Alfajor individual",
                precio_base=Decimal("1200.00"),
                unidad_venta_id=unidad_por_nombre["pieza"].id,
                stock_cantidad=Decimal("30"),  # noqa: FURB157
                disponible=True,
            ),
            Producto(
                nombre="Porcion de torta",
                descripcion="Porcion individual de torta",
                precio_base=Decimal("3500.00"),
                unidad_venta_id=unidad_por_nombre["pieza"].id,
                stock_cantidad=Decimal("12"),  # noqa: FURB157
                disponible=True,
            ),

            # Docena
            Producto(
                nombre="Facturas surtidas",
                descripcion="Docena de facturas surtidas",
                precio_base=Decimal("8500.00"),
                unidad_venta_id=unidad_por_nombre["docena"].id,
                stock_cantidad=Decimal("8"),  # noqa: FURB157
                disponible=True,
            ),
            Producto(
                nombre="Medialunas",
                descripcion="Docena de medialunas",
                precio_base=Decimal("7800.00"),
                unidad_venta_id=unidad_por_nombre["docena"].id,
                stock_cantidad=Decimal("6"),  # noqa: FURB157
                disponible=True,
            ),
        ]

        session.add_all(productos)
        session.commit()