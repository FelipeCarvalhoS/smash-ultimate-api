from fastapi import Query
from pydantic import BaseModel
from enum import StrEnum
from .shared import SmashGames, Series


class Availability(StrEnum):
    STARTER = 'Starter'
    FREE_DLC = 'Free DLC'
    PAID_DLC = 'Paid DLC'


class Stage(BaseModel):
    id: int
    name: str
    slug: str
    series: Series
    availability: Availability
    also_appears_in: list[SmashGames]
    image: str
    is_original_or_new_version: bool

    model_config = {'extra': 'forbid'}


class StageQueryParams(BaseModel):
    id: list[int] | None = Query(default=None, description='List of IDs')
    name: list[str] | None = Query(default=None, description='List of names')
    series: list[Series] | None = Query(default=None, description='List of series')
    availability: list[Availability] | None = Query(default=None, description='List of availabilities')
    also_appears_in: list[SmashGames] | None = Query(default=None, description='List of Smash games it also appears in')
    is_original_or_new_version: bool | None = Query(default=None, description='Whether the stage must be original or a new version')