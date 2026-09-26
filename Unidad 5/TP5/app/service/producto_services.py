from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate
from fastapi import HTTPException, status
from sqlmodel import Session, select


def crear_producto(session: Session, data: ProductoCreate) -> Producto:
    # Validación: nombre único 
    existe = session.exec(
        select(Producto).where(Producto.nombre == data.nombre)
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


def listar_productos(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    activo: bool | None = None,
) -> list[Producto]:

    query = select(Producto)

    if activo is not None:
        query = query.where(Producto.activo == activo)

    query = query.offset(skip).limit(limit)
    return list(session.exec(query).all())


def obtener_producto_por_id(session: Session, producto_id: int) -> Producto:
    producto = session.get(Producto, producto_id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    return producto


def actualizar_producto(session: Session, producto_id: int, data: ProductoUpdate) -> Producto:
    producto = obtener_producto_por_id(session, producto_id)

    cambios = data.model_dump(exclude_unset=True)
    producto.sqlmodel_update(cambios)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def desactivar_producto(session: Session, producto_id: int) -> Producto:
    producto = obtener_producto_por_id(session, producto_id)

    if not producto.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya está inactivo",
        )

    producto.activo = False
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def obtener_estado_stock(session: Session, producto_id: int):
    producto = obtener_producto_por_id(session, producto_id)

    bajo_minimo = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": bajo_minimo,
        "activo": producto.activo,
    }
