from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db
from app.modules.categorias.router import router as categoria_router
from app.modules.productos.router import router as producto_router
from app.modules.unidades_medida.router import router as unidad_medida_router
from app.core.seed import seed_unidades_medida


def create_app() -> FastAPI:
    app = FastAPI(
        title="API 2do parcial - Programacion 4",
        description="Parcial de Desarrollo.",
        version="1.0.0",
    )
    
    # Crear tablas al iniciar la app
    create_db()
    
    # Carga inicial de medidas
    seed_unidades_medida()
    
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
    app.include_router(unidad_medida_router)

    return app


app = create_app()
