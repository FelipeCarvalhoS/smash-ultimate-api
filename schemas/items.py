from fastapi import Query
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
    id: list[int] | None = Query(default=None, description='List of IDs')
    name: list[str] | None = Query(default=None, description='List of names')
    series: list[Series] | None = Query(default=None, description='List of series')
    also_appears_in: list[SmashGames] | None = Query(default=None, description='List of Smash games it also appears in')
    types: list[ItemType] | None = Query(default=None, description='List of types')
    heavy: bool | None = Query(default=None, description='Whether the item must be heavy or not')