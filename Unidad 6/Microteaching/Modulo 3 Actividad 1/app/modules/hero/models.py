from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.modules.weapon.models import Weapon


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    weapon_id: int | None = Field(
        default=None,
        foreign_key="weapon.id",
        unique=True
    )

    weapon: Weapon | None = Relationship(back_populates="hero")