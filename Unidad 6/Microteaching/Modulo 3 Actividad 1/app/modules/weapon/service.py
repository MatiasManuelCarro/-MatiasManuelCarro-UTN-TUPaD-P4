from sqlmodel import Session
from app.modules.weapon.models import Weapon
from app.modules.weapon.schemas import WeaponCreate


def create_weapon(session: Session, weapon_data: WeaponCreate):
    weapon = Weapon(**weapon_data.model_dump())
    session.add(weapon)
    session.commit()
    session.refresh(weapon)
    return weapon