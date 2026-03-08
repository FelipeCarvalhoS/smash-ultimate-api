from pydantic import BaseModel
from enum import StrEnum
from .shared import SmashGames, Series


class ItemType(StrEnum):
    BATTERING = 'Battering'
    SPECIAL = 'Special'
    EXPLOSIVE = 'Explosive'
    SHOOTING = 'Shooting'
    THROWING = 'Throwing'
    TRANSFORMATION = 'Transformation'
    CONTAINER = 'Container'
    RECOVERY = 'Recovery'
    SUMMONING = 'Summoning'
    STATUS = 'Status'


class Item(BaseModel):
    id: int
    name: str
    slug: str
    series: Series
    also_appears_in: list[SmashGames]
    image: str
    types: list[ItemType]
    heavy: bool
    notes: str

    model_config = {'extra': 'forbid'}


class ItemQueryParams(BaseModel):
    ids: list[int] | None = None
    names: list[str] | None = None
    series: list[Series] | None = None
    also_appears_in: list[SmashGames] | None = None
    types: list[ItemType] | None = None
    heavy: bool | None = None