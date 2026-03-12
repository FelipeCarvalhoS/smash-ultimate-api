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
    id: list[int] | None = None
    name: list[str] | None = None
    series: list[Series] | None = None
    availability: list[Availability] | None = None
    also_appears_in: list[SmashGames] | None = None
    is_original_or_new_version: bool | None = None