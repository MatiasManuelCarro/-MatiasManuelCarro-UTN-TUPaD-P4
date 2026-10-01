from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.modules.hero.models import Hero


class Weapon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    hero: Optional["Hero"] = Relationship(back_populates="weapon")