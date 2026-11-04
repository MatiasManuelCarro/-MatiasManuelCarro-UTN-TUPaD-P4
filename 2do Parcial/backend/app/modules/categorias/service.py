from app.modules.categorias.schema import CategoriaCreate, CategoriaPublic
from sqlmodel import Session, select
from app.modules.categorias.model import Categoria
from fastapi import HTTPException, status

#POST /api/v1/categorias
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

# GET /api/v1/categorias