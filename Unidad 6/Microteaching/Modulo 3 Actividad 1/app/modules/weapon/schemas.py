from sqlmodel import SQLModel


class WeaponCreate(SQLModel):
    name: str