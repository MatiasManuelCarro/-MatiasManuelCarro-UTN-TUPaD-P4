from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.categoria.router import router as categoria_router
from app.core.database import create_db
from app.producto.router import router as producto_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="API Integradora - Unidad 6",
        description="Relaciones, Estado, CRUD.",
        version="1.0.0",
    )
    
    # Crear tablas al iniciar la app
    create_db()
    
    # Habilitar CORS para el front-end (Vite)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.include_router(producto_router)
    app.include_router(categoria_router)

    return app


app = create_app()
