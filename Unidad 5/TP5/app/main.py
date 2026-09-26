from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db  #Función actual
from app.routers.categoria import router as categoria_router

# ! cuando este producto y proveedor:
# from app.routers.producto import router as producto_router
# from app.routers.proveedor import router as proveedor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al levantar el servidor: crea las tablas si no existen.
    create_db()
    yield


app = FastAPI(
    title="TP5 - Gestión de Productos",
    description="CRUD persistente de Categorías, Productos y Proveedores con SQLModel + PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)

# Routers
app.include_router(categoria_router)
# * app.include_router(producto_router)
# * app.include_router(proveedor_router)


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "API TP5 funcionando. Ver /docs para la documentación interactiva."}
