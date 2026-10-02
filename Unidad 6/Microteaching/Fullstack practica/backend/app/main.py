from app.routes.autores import router as autores_router
from app.routes.libros import router as libros_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(autores_router)
app.include_router(libros_router)

#levantar backend
# python -c "from app.database import crear_tablas; crear_tablas()"
# uvicorn app.main:app --reload
