import uvicorn
from app.turnos import router as turnos_router
from fastapi import FastAPI

app = FastAPI()



app.include_router(turnos_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
