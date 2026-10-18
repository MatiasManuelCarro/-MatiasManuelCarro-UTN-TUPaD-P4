from sqlmodel import SQLModel


class WeaponBase(SQLModel):
    name: str
    description: str | None = None


class WeaponCreate(WeaponBase):
    pass


class WeaponRead(WeaponBase):
    id: int


class WeaponUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
 

#Paginado
class WeaponPaginatedResponse(SQLModel):
    total: int
    items: list[WeaponRead] 