from app.ambulancias import router as ambulancias_router
from app.categorias import router as categorias_router
from app.controles import router as controles_router
from app.insumos import router as insumos_router
from app.turnos import router as turnos_router
from app.usuarios import router as usuarios_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mock Backend TFI",
    version="1.0.0"
)


# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # permite que el front lea la respuesta
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registrar routers
app.include_router(usuarios_router)
app.include_router(ambulancias_router)
app.include_router(insumos_router)
app.include_router(categorias_router)
app.include_router(turnos_router)
app.include_router(controles_router)


@app.get("/")
def root():
    return {"status": "Mock Backend TFI funcionando"}
