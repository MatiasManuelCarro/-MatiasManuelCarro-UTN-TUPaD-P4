from datetime import datetime

from app.modules.productos.model import Producto, ProductoCategoria
from app.modules.productos.schema import ProductoCreate, ProductoPublic, ProductoUpdate
from app.modules.unidades_medida.model import UnidadMedida
from fastapi import HTTPException, status
from sqlmodel import Session, select


# POST /api/v1/productos
def crear_producto(session: Session, data: ProductoCreate) -> Producto:

    # RN-03 Verificacion de existencia de unidad medida
    unidad = session.get(UnidadMedida, data.unidad_venta_id)

    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada",
        )

    # Validacion de nombre único
    existe = session.exec(
        select(Producto).where(Producto.nombre == data.nombre, Producto.activo == True)
    ).first()

    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un producto con nombre: {data.nombre}",
        )

    nuevo_producto = Producto(**data.model_dump())
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)

    return nuevo_producto


# GET /api/v1/productos
def listar_productos(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    activo: bool | None = None,
    disponible: bool | None = None,
    categoria_id: int | None = None,
    search: str | None = None,
) -> list[Producto]:

    query = select(Producto)

    if activo is False:
        query = query.where(Producto.activo == False)
    else:
        query = query.where(Producto.activo == True)

    if disponible is not None:
        query = query.where(Producto.disponible == disponible)

    if search is not None and search.strip():
        query = query.where(Producto.nombre.ilike(f"%{search}%"))

    if categoria_id is not None:
        query = (
            query.join(ProductoCategoria, Producto.id == ProductoCategoria.producto_id)
            .where(ProductoCategoria.categoria_id == categoria_id)
            .distinct()
        )

    query = query.offset(skip).limit(limit)

    productos = session.exec(query).all()

    return [
        ProductoPublic(
            **producto.model_dump(),
            unidad_venta=producto.unidad_venta,
            categorias=producto.categorias,
            hay_stock=producto.stock_cantidad > 0,
        )
        for producto in productos
    ]


# GET /api/v1/productos/{id}
def obtener_producto_por_id(session: Session, producto_id: int) -> Producto:
    producto = session.get(Producto, producto_id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    return producto


# PUT /api/v1/productos/{id}
def actualizar_producto(
    session: Session, producto_id: int, data: ProductoUpdate
) -> Producto:
    producto = obtener_producto_por_id(session, producto_id)

    cambios = data.model_dump()

    if not producto.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede modificar un producto que no esta activo",
        )
    
    unidad = session.get(UnidadMedida, data.unidad_venta_id)

    # RN-03
    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada",
        )

    if "nombre" in cambios:
        producto_existente = session.exec(
            select(Producto).where(
                Producto.nombre == cambios["nombre"],
                Producto.activo == True,
                Producto.id != producto_id,
            )
        ).first()

        if producto_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un producto activo con ese nombre",
            )

    producto.sqlmodel_update(cambios)

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto


# DELETE /api/v1/productos/{id}
def desactivar_producto(session: Session, producto_id: int) -> Producto:
    producto = obtener_producto_por_id(session, producto_id)

    if not producto.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya no esta activo",
        )

    producto.activo = False
    producto.anulado_at = datetime.now()

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
