from sqlmodel import SQLModel

from app.modules.weapon.schemas import WeaponRead


# ─── Base ──────────────────────────────────────────────────────────────────
class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None


# ─── Request schemas ───────────────────────────────────────────────────────
class HeroCreate(HeroBase):
    team_id: int | None = None      # 1:N  – asignar equipo principal
    weapon_id: int | None = None    # 1:1  – asignar arma


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    team_id: int | None = None
    weapon_id: int | None = None


# ─── Response schemas ──────────────────────────────────────────────────────
class HeroRead(HeroBase):
    id: int
    team_id: int | None = None
    weapon_id: int | None = None


class TeamBasicRead(SQLModel):
    """Schema reducido de Team para evitar import circular en schemas."""
    id: int
    name: str
    headquarters: str


class HeroReadFull(HeroRead):
    """Hero con todas sus relaciones anidadas."""
    weapon: WeaponRead | None = None
    team: TeamBasicRead | None = None
    teams: list[TeamBasicRead] = []


# ─── Operaciones N:M ──────────────────────────────────────────────────────
class HeroTeamAssign(SQLModel):
    team_id: int
