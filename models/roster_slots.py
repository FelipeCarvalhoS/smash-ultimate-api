from pydantic import BaseModel
from enum import StrEnum


class SmashGames(StrEnum):
    SSB = '64'
    MELEE = 'Melee'
    BRAWL = 'Brawl'
    SSB4 = 'Smash 4'


class Availability(StrEnum):
    STARTER = 'Starter'
    UNLOCKABLE = 'Unlockable'
    DLC = 'DLC'


class Tip(BaseModel):
    title: str
    content: str


class Alt(BaseModel):
    slot: int
    variant: str


class VariantType(StrEnum):
    DEFAULT = 'Default'
    SAME_CHARACTER = 'Same character'
    DIFFERENT_CHARACTER = 'Different character'


class Variant(BaseModel):
    name: str
    boxing_ring_title: str
    type: VariantType


class Fighter(BaseModel):
    id: str
    name: str
    also_appears_in: list[SmashGames]


class RosterSlot(BaseModel):
    ids: list[str]
    name: str
    series: str
    availability: Availability
    also_appears_in: list[SmashGames]
    alts: list[Alt]
    variants: list[Variant]
    tips: list[Tip]
    fighters: list[Fighter]
