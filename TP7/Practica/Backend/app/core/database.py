from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# URL de conexión a PostgreSQL
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/tp_unidad_7"

engine = create_engine(
    DATABASE_URL,
    echo=True,            # mSQL en consola 
)


# Sesión de SQLModel
def get_session():
    with Session(engine) as session:
        yield session


# Dependencia para FastAPI
SessionDep = Annotated[Session, Depends(get_session)]


# Crear tablas (opcional, útil para desarrollo)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
