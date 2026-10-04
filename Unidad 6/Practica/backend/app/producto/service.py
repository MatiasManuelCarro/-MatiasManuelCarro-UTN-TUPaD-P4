
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.producto.model import Producto
from app.producto.schema import ProductoCreate, ProductoUpdate


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
    disponible: bool | None = None,
) -> list[Producto]:

    query = select(Producto)

    if disponible is not None:
        query = query.where(Producto.disponible == disponible)

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

    if not producto.disponible:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya está marcado como no disponible",
        )

    producto.disponible = False
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

def eliminar_producto(session: Session, producto_id: int) -> None:
    producto = session.get(Producto, producto_id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    session.delete(producto)
    session.commit()