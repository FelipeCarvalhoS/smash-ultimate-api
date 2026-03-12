from fastapi import Query
from pydantic import BaseModel
from enum import StrEnum
from utils import get_snippet
from .shared import SmashGames, Series
from .fighters import Fighter


class Availability(StrEnum):
    STARTER = 'Starter'
    UNLOCKABLE = 'Unlockable'
    PAID_DLC = 'Paid DLC'
    CUSTOM = 'Custom'


class TipLevel(StrEnum):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'


class Tip(BaseModel):
    title: str
    content: str
    level: TipLevel

    model_config = {'extra': 'forbid'}


class Alt(BaseModel):
    slot: int
    variant: str
    image: str

    model_config = {'extra': 'forbid'}


class VariantType(StrEnum):
    DEFAULT = 'Default'
    SAME_CHARACTER = 'Same character'
    DIFFERENT_CHARACTER = 'Different character'


class Variant(BaseModel):
    name: str
    boxing_ring_title: str
    type: VariantType

    model_config = {'extra': 'forbid'}


class RosterSlot(BaseModel):
    ids: list[str]
    name: str
    slug: str
    series: Series
    availability: Availability
    also_appears_in: list[SmashGames]
    order: int
    alts: list[Alt]
    variants: list[Variant]
    tips: list[Tip]
    fighters: list[Fighter]

    model_config = {'extra': 'forbid'}


class RosterSlotQueryParams(BaseModel):
    ids: list[str] | None = None
    names: list[str] | None = None
    series: list[Series] | None = None
    availability: list[Availability] | None = None
    also_appears_in: list[SmashGames] | None = None
