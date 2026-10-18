import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
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
