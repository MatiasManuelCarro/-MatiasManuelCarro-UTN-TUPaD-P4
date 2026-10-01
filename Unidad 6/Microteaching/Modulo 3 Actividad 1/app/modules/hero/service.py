from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.modules.hero.models import Hero
from app.modules.hero.schemas import HeroCreate


def create_hero(session: Session, hero_data: HeroCreate):
    hero = Hero(**hero_data.model_dump())
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


def get_hero(session: Session, hero_id: int):
    statement = (
        select(Hero)
        .where(Hero.id == hero_id)
        .options(selectinload(Hero.weapon))
    )
    return session.exec(statement).first()