from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ambulancias import router as ambulancias_router
from app.controles import router as controles_router
from app.insumos import router as insumos_router
from app.turnos import router as turnos_router
from app.usuarios import router as usuarios_router

app = FastAPI(title="Mock Sistema Gestión 107")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)
app.include_router(ambulancias_router)
app.include_router(insumos_router)
app.include_router(turnos_router)
app.include_router(controles_router)

@app.get("/")
def root():
    return {"mensaje": "Mock 107 activo"}
