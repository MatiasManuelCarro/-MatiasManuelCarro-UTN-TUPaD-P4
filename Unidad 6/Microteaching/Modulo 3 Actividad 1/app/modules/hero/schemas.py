from typing import Optional
from sqlmodel import SQLModel


class HeroCreate(SQLModel):
    name: str
    weapon_id: Optional[int] = None