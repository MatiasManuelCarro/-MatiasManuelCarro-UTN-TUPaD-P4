from datetime import UTC, datetime

from app.categoria.model import Categoria
from app.producto.model import Producto
from app.producto.schema import (
    ProductoCreate,
    ProductoPaginatedResponse,
    ProductoPublic,
    ProductoUpdate,
)
from app.producto_categoria.model import ProductoCategoria
from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlmodel import Session, select


def crear_producto(session: Session, data: ProductoCreate):
    existente = session.exec(
        select(Producto)
        .where(Producto.nombre == data.nombre)
        .where(Producto.deleted_at.is_(None))
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un producto con nombre '{data.nombre}'",
        )

    campos = data.model_dump()
    categorias_ids = campos.pop("categorias", [])

    nuevo = Producto(**campos)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)

    # Crear relaciones N:M
    for cat_id in categorias_ids:
        categoria = session.get(Categoria, cat_id)
        if not categoria or categoria.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría {cat_id} no existe",
            )

        session.add(ProductoCategoria(producto_id=nuevo.id, categoria_id=cat_id))

    session.commit()

    # Construir respuesta compatible con ProductoPublic
    categorias_rel = session.exec(
        select(ProductoCategoria).where(ProductoCategoria.producto_id == nuevo.id)
    ).all()

    return {
        **nuevo.model_dump(),
        "categorias": [rel.categoria_id for rel in categorias_rel],
    }


def listar_productos(
    session: Session,
    offset: int,
    limit: int,
    nombre: str | None,
    incluir_inactivos: bool,
) -> ProductoPaginatedResponse:

    query = select(Producto)

    if not incluir_inactivos:
        query = query.where(Producto.deleted_at.is_(None))

    if nombre:
        query = query.where(Producto.nombre.ilike(f"%{nombre}%"))

    resultados = session.exec(query).all()

    total = len(resultados)

    productos_orm = resultados[offset : offset + limit]

    items = []
    for prod in productos_orm:
        prod_dict = prod.model_dump()
        prod_dict["categorias"] = [c.id for c in prod.categorias]
        items.append(ProductoPublic(**prod_dict))

    return ProductoPaginatedResponse(total=total, items=items)


def obtener_producto_por_id(session: Session, producto_id: int) -> Producto:
    producto = session.exec(
        select(Producto)
        .where(Producto.id == producto_id)
        .where(Producto.deleted_at.is_(None))
    ).first()

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto


def actualizar_producto(
    session: Session, producto_id: int, data: ProductoUpdate
) -> Producto:
    producto = obtener_producto_por_id(session, producto_id)
    cambios = data.model_dump(exclude_unset=True)

    categorias_ids = cambios.pop("categorias", None)

    # Actualizar campos del producto
    producto.sqlmodel_update(cambios)
    producto.updated_at = datetime.now(UTC)

    session.add(producto)
    session.commit()
    session.refresh(producto)

    # Si el usuario NO envió categorias, no modifica relaciones
    if categorias_ids is None:
        return producto

    # Reemplazar relaciones: eliminar todas y crear nuevas
    session.exec(
        delete(ProductoCategoria).where(ProductoCategoria.producto_id == producto.id)
    )

    # Crear nuevas relaciones
    for cat_id in categorias_ids:
        categoria = session.get(Categoria, cat_id)
        if not categoria or categoria.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría {cat_id} no existe",
            )

        session.add(ProductoCategoria(producto_id=producto.id, categoria_id=cat_id))

    session.commit()
    # Convertir categorías a IDs para el response_model
    categorias_rel = session.exec(
        select(ProductoCategoria).where(ProductoCategoria.producto_id == producto.id)
    ).all()

    return {
        **producto.model_dump(),
        "categorias": [rel.categoria_id for rel in categorias_rel],
    }


def eliminar_producto(session: Session, producto_id: int) -> None:
    producto = session.get(Producto, producto_id)

    if not producto or producto.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )

    producto.deleted_at = datetime.now(UTC)
    session.add(producto)
    session.commit()
