from fastapi import APIRouter
from app.database import SessionDep
from app.models import Libro
from app.schemas import LibroCreate, LibroRead

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=LibroRead)
def crear_libro(data: LibroCreate, session: SessionDep):
    libro = Libro(titulo=data.titulo, autor_id=data.autor_id)
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro
