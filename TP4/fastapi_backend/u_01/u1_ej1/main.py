from fastapi import FastAPI

# Inicializamos la aplicación
app = FastAPI()

# Definimos la ruta raíz (GET)
@app.get("/")
async def root():
    return {"message": "Hello World"}
  
@app.get("/ping")
async def ping():
    return {"status": "ok", "ts": "2026-02-08"}