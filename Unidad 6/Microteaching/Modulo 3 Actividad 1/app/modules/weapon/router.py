from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.modules.weapon.schemas import WeaponCreate
from app.modules.weapon import service

router = APIRouter(prefix="/weapons", tags=["Weapons"])


@router.post("/")
def create_weapon(
    weapon: WeaponCreate,
    session: Session = Depends(get_session)
):
    return service.create_weapon(session, weapon)