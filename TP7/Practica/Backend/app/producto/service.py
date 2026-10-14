from datetime import datetime, timezone

from app.producto.model import Producto
from app.producto.schema import ProductoCreate, ProductoUpdate
from fastapi import HTTPException, status
from sqlmodel import Session, select


def crear_producto(session: Session, data: ProductoCreate) -> Producto:
    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def listar_productos(session: Session, skip: int = 0, limit: int = 10) -> list[Producto]:
    query = (
        select(Producto)
        .where(Producto.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    return session.exec(query).all()


def obtener_producto_por_id(session: Session, producto_id: int) -> Producto:
    producto = session.exec(
        select(Producto)
        .where(Producto.id == producto_id)
        .where(Producto.deleted_at.is_(None))
    ).first()

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto


def actualizar_producto(session: Session, producto_id: int, data: ProductoUpdate) -> Producto:
    producto = obtener_producto_por_id(session, producto_id)
    cambios = data.model_dump(exclude_unset=True)

    producto.sqlmodel_update(cambios)
    producto.updated_at = datetime.now(timezone.utc)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def eliminar_producto(session: Session, producto_id: int) -> None:
    producto = session.get(Producto, producto_id)

    if not producto or producto.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    producto.deleted_at = datetime.now(timezone.utc)
    session.add(producto)
    session.commit()
