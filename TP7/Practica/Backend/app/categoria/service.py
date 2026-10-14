from datetime import datetime, timezone

from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate
from fastapi import HTTPException, status
from sqlmodel import Session, select


def crear_categoria(session: Session, data: CategoriaCreate) -> Categoria:
    existe = session.exec(
        select(Categoria)
        .where(Categoria.nombre == data.nombre)
        .where(Categoria.deleted_at.is_(None))
    ).first()

    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe categoría con nombre: {data.nombre}",
        )

    nueva = Categoria(**data.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


def listar_categorias(session: Session, skip: int = 0, limit: int = 10) -> list[Categoria]:
    query = (
        select(Categoria)
        .where(Categoria.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    return session.exec(query).all()


def obtener_categoria_por_id(session: Session, categoria_id: int) -> Categoria:
    categoria = session.exec(
        select(Categoria)
        .where(Categoria.id == categoria_id)
        .where(Categoria.deleted_at.is_(None))
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    return categoria


def actualizar_categoria(session: Session, categoria_id: int, data: CategoriaUpdate) -> Categoria:
    categoria = obtener_categoria_por_id(session, categoria_id)
    cambios = data.model_dump(exclude_unset=True)

    categoria.sqlmodel_update(cambios)
    categoria.updated_at = datetime.now(timezone.utc)

    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def eliminar_categoria(session: Session, categoria_id: int) -> None:
    categoria = session.get(Categoria, categoria_id)

    if not categoria or categoria.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )

    if categoria.productos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la categoría porque tiene productos asociados",
        )

    categoria.deleted_at = datetime.now(timezone.utc)
    session.add(categoria)
    session.commit()
