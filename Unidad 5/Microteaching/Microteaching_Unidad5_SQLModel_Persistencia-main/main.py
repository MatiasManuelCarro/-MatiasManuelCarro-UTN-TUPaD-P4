from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db_and_tables
from app.routers import paciente, turno


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al levantar el servidor: crea las tablas si no existen.
    create_db_and_tables()
    yield


app = FastAPI(
    title="API Consultorio - Gestión de Turnos",
    description="CRUD persistente de Pacientes y Turnos sobre PostgreSQL, con SQLModel.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(paciente.router)
app.include_router(turno.router)


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "API de gestión de turnos de consultorio. Ver /docs para la documentación interactiva."}


