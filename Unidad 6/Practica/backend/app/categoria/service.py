from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate


def crear_categoria(session: Session, data: CategoriaCreate) -> Categoria:
    existe = session.exec(
        select(Categoria).where(Categoria.nombre == data.nombre)
    ).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe categotia con nombre: {data.nombre}",
        )
    nueva_categoria = Categoria(**data.model_dump())
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria


def listar_categorias(
    session: Session,
    skip: int = 0,
    limit: int = 10,
) -> list[Categoria]:
    query = select(Categoria).offset(skip).limit(limit)
    return session.exec(query).all()

def obtener_categoria_por_id(session: Session, categoria_id: int) -> Categoria:
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada"
        )
    return categoria


def actualizar_categoria(session: Session, categoria_id: int, data: CategoriaUpdate) -> Categoria:
    categoria = obtener_categoria_por_id(session, categoria_id)
    cambios = data.model_dump(exclude_unset=True)
    categoria.sqlmodel_update(cambios)
    
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def desactivar_categoria(session: Session, categoria_id: int) -> Categoria:
    """Baja lógica: no borra la Categoria, lo marca inactivo."""
    categoria = obtener_categoria_por_id(session, categoria_id)
    
    if not categoria.activo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La categoria ya está inactiva")

    categoria.activo = False
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

def eliminar_categoria(session: Session, categoria_id: int) -> None:
    categoria = session.get(Categoria, categoria_id)

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    # Si tiene productos asociados → no permitir eliminar
    if categoria.productos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la categoría porque tiene productos asociados"
        )

    session.delete(categoria)
    session.commit()