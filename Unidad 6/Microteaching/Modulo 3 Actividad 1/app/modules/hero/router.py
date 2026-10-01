from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.modules.hero.schemas import HeroCreate
from app.modules.hero import service

router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.post("/")
def create_hero(
    hero: HeroCreate,
    session: Session = Depends(get_session)
):
    return service.create_hero(session, hero)


@router.get("/{hero_id}")
def read_hero(
    hero_id: int,
    session: Session = Depends(get_session)
):
    return service.get_hero(session, hero_id)