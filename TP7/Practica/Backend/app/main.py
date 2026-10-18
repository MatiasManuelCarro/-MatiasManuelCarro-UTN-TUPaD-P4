from app.categoria.router import router as categoria_router
from app.core.database import SessionDep, create_db_and_tables
from app.producto.router import router as producto_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

app = FastAPI()

create_db_and_tables()

# CORS restringido solo al frontend Vite
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # solo Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers del dominio Catálogo
app.include_router(categoria_router)
app.include_router(producto_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db(session: SessionDep):
    session.exec(text("SELECT 1"))
    return {"status": "ok"}