# run.py
import os
import sys
import uvicorn

# Asegurar que backend/ esté en el PYTHONPATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app.database import crear_tablas

print("Creando tablas en la base de datos...")
crear_tablas()
print("Tablas creadas correctamente.\n")

print("Levantando FastAPI en http://localhost:8000 ...\n")

# Ejecutar uvicorn directamente, sin subprocess
uvicorn.run(
    "app.main:app",
    host="127.0.0.1",
    port=8000,
    reload=False,   
)
