from enum import Enum
from fastapi import FastAPI


app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name}
