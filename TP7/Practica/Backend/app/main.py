from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router
from app.producto_categoria.router import router as producto_categoria_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
app.include_router(producto_categoria_router)
