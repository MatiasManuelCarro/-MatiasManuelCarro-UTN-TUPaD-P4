# run.py
import pytest
import uvicorn
from app.database import create_db


def init_db():
    print("Creando tablas en la base de datos...\n")
    create_db()
    print("Tablas creadas correctamente.\n")

def start_api():
    print("Levantando API en http://localhost:8000 ...\n")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

def run_tests():
    print("Ejecutando tests...\n")
    pytest.main(["-x", "tests"])

if __name__ == "__main__":
    init_db()
    start_api()
