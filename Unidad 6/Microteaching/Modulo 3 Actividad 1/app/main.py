from contextlib import asynccontextmanager

from app.core.database import engine
from app.modules.hero.models import Hero
from app.modules.hero.router import router as hero_router
from app.modules.weapon.models import Weapon
from app.modules.weapon.router import router as weapon_router
from fastapi import FastAPI
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(hero_router)
app.include_router(weapon_router)