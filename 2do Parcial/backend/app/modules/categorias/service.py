from datetime import datetime

from app.modules.categorias.model import Categoria
from app.modules.categorias.schema import (
    CategoriaCreate,
    CategoriaPublic,
    CategoriaUpdate,
)
from fastapi import HTTPException, status
from sqlmodel import Session, select


# * POST /api/v1/categorias
def crear_categorias(
    session: Session,
    data: CategoriaCreate
) -> CategoriaPublic:
    
    # RN-02: nombre unico entre categorias activas
    existe = session.exec(
        select(Categoria).where(
            Categoria.nombre == data.nombre,
            Categoria.activo == True
        )
    ).first()
    
    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una categoria activa con ese nombre"
        )
    
    nueva_categoria = Categoria(**data.model_dump())
    
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    
    return CategoriaPublic(
        **nueva_categoria.model_dump()
    )

# * GET /api/v1/categorias
def listar_categorias(
    session: Session,
    activo: bool | None = None,
    search: str | None = None
) -> list[CategoriaPublic]:
    
    query = select(Categoria)
    
    if activo is False:
        query = query.where(Categoria.activo == False)
    else:
        query = query.where(Categoria.activo == True)
    
    if search is not None and search.strip():
        query = query.where(
            Categoria.nombre.ilike(f"%{search}%")         
        )
    
    categorias = session.exec(query).all()
    
    return[CategoriaPublic(
        **categoria.model_dump()
        )for categoria in categorias
    ]

# * GET /api/v1/categorias/{id}
def obtener_categorias_por_id(
    session: Session,
    categoria_id: int
) -> Categoria:
    
    categoria = session.get(Categoria, categoria_id)
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria no encontrada"
        )
    return categoria

# * PUT /api/v1/categorias/{id}
def actualizar_categoria(
    session: Session,
    categoria_id: int,
    data: CategoriaUpdate
) -> CategoriaPublic:
    
    # RN-03 y RN-05 - no se puede consultar o modificar si esta anulada
    categoria = obtener_categorias_por_id(session, categoria_id)
    
    if not categoria.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede modificar una categoria anulada"
        )
    
    # RN-02 - nombre unico entre categorias activas
    categoria_existente = session.exec(
        select(Categoria).where(
            Categoria.nombre == data.nombre,
            Categoria.activo == True,
            Categoria.id != categoria_id,
        )
    ).first()
    
    if categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una categoria activa con ese nombre"
        )
    
    categoria.sqlmodel_update(data.model_dump())
    
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    
    return CategoriaPublic(
        **categoria.model_dump()
    )

# DELETE /api/v1/categorias/{id}
def desactivar_categoria(
    session: Session,
    categoria_id: int
) -> Categoria:
    
    # RN-03 - RN-04 No puede consultar una categoria inactiva - no se puede desactivar si ya esta inactiva
    
    categoria = obtener_categorias_por_id(session, categoria_id)
    
    if not categoria.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La categoria esta anulada"
        )
    
    categoria.activo = False
    categoria.anulado_at = datetime.now()
    
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    
    return categoria