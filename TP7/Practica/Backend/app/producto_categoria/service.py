from app.categoria.model import Categoria
from app.producto.model import Producto
from app.producto_categoria.model import ProductoCategoria
from fastapi import HTTPException, status
from sqlmodel import Session, select


def crear_relacion(session: Session, data):

    # Validar producto
    producto = session.get(Producto, data.producto_id)  # noqa: F821
    if not producto or producto.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {data.producto_id} no existe"
        )

    # Validar categoría
    categoria = session.get(Categoria, data.categoria_id)
    if not categoria or categoria.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría {data.categoria_id} no existe"
        )

    # Validar relación duplicada
    existe = session.exec(
        select(ProductoCategoria).where(
            ProductoCategoria.producto_id == data.producto_id,
            ProductoCategoria.categoria_id == data.categoria_id,
        )
    ).first()

    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La relación ya existe"
        )

    nueva = ProductoCategoria(**data.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


def listar_relaciones(session: Session):
    return session.exec(select(ProductoCategoria)).all()


def eliminar_relacion(session: Session, producto_id: int, categoria_id: int):
    relacion = session.get(ProductoCategoria, (producto_id, categoria_id))
    if not relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación no encontrada"
        )

    session.delete(relacion)
    session.commit()
