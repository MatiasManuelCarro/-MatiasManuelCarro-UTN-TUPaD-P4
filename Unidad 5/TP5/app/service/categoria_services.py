from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from fastapi import HTTPException, status
from sqlmodel import Session, select


def crear_categoria(session: Session, data: CategoriaCreate) -> Categoria:
    existe = session.exec(
        select(Categoria).where(Categoria.codigo == data.codigo)
    ).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe categotia con codigo: {data.codigo}",
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
    activo: bool | None = None,
) -> list[Categoria]:
    query = select(Categoria)
    if activo is not None:
        query = query.where(Categoria.activo == activo)
    query = query.offset(skip).limit(limit)
    return list(session.exec(query).all())


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