"""
Capa de persistencia: configuración del engine, creación de tablas
e inyección de sesión por request.

Sigue el mismo patrón visto en la unidad: una única instancia global
del engine, una Session por petición vía Depends, y create_db_and_tables()
ejecutada al levantar la aplicación.
"""

import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:1234@localhost:5432/turnos_db",
)

# echo=True muestra las consultas SQL generadas; útil en desarrollo,
# se puede apagar en producción.
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Inspecciona los modelos con table=True y crea las tablas si no existen."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Crea una sesión nueva por cada request y la cierra al finalizar."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
