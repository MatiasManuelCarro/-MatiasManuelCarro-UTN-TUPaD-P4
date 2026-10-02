from fastapi import APIRouter
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.database import SessionDep
from app.models import Autor
from app.schemas import AutorCreate, AutorRead, AutorReadWithLibros

router = APIRouter(prefix="/autores", tags=["Autores"])

@router.post("/", response_model=AutorRead)
def crear_autor(data: AutorCreate, session: SessionDep):
    autor = Autor(nombre=data.nombre)
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor


@router.get("/", response_model=list[AutorReadWithLibros])
def listar_autores(session: SessionDep):
    query = select(Autor).options(selectinload(Autor.libros))
    return session.exec(query).all()
