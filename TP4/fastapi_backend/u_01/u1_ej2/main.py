from enum import Enum

from fastapi import FastAPI

app = FastAPI()

# ⚠️ IMPORTANTE: El orden de las rutas importa en FastAPI

# 1. Ruta estática (Debe ir primero)
@app.get("/user/me")
async def read_user_me():
    return {"user": "current"}

# 2. Ruta dinámica (Debe ir después)
@app.get("/user/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# Le indicamos a Python que item_id DEBE ser un entero (int)
@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

#ENUMS# 
#
# . Creamos una clase que hereda de str y de Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# 2. Usamos nuestra clase como Type Hint
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # FastAPI ya validó que model_name solo puede ser uno de los 3 permitidos
    return {"model_name": model_name}



