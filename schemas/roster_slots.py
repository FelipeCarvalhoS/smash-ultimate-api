from pydantic import BaseModel
from enum import StrEnum


class Series(StrEnum):
    ARMS = 'ARMS'
    ANIMAL_CROSSING = 'Animal Crossing'
    BANJO_KAZOOIE = 'Banjo-Kazooie'
    BAYONETTA = 'Bayonetta'
    CASTLEVANIA = 'Castlevania'
    DONKEY_KONG = 'Donkey Kong'
    DRAGON_QUEST = 'Dragon Quest'
    DUCK_HUNT = 'Duck Hunt'
    EARTHBOUND = 'EarthBound'
    F_ZERO = 'F-Zero'
    FATAL_FURY = 'Fatal Fury'
    FINAL_FANTASY = 'Final Fantasy'
    FIRE_EMBLEM = 'Fire Emblem'
    GAME_AND_WATCH = 'Game & Watch'
    ICE_CLIMBER = 'Ice Climber'
    KID_ICARUS = 'Kid Icarus'
    KINGDOM_HEARTS = 'Kingdom Hearts'
    KIRBY = 'Kirby'
    MARIO = 'Mario'
    MEGA_MAN = 'Mega Man'
    METAL_GEAR = 'Metal Gear'
    METROID = 'Metroid'
    MINECRAFT = 'Minecraft'
    PAC_MAN = 'Pac-Man'
    PERSONA = 'Persona'
    PIKMIN = 'Pikmin'
    POKEMON = 'Pokémon'
    PUNCH_OUT = 'Punch-Out!!'
    ROB = 'R.O.B.'
    SONIC = 'Sonic'
    SPLATOON = 'Splatoon'
    STAR_FOX = 'Star Fox'
    STREET_FIGHTER = 'Street Fighter'
    SUPER_SMASH_BROS = 'Super Smash Bros.'
    TEKKEN = 'Tekken'
    THE_LEGEND_OF_ZELDA = 'The Legend of Zelda'
    WARIO = 'Wario'
    WII_FIT = 'Wii Fit'
    XENOBLADE_CHRONICLES = 'Xenoblade Chronicles'
    YOSHI = 'Yoshi'



class SmashGames(StrEnum):
    SSB = '64'
    MELEE = 'Melee'
    BRAWL = 'Brawl'
    SSB4 = 'Smash 4'


class Availability(StrEnum):
    STARTER = 'Starter'
    UNLOCKABLE = 'Unlockable'
    DLC = 'DLC'
    CUSTOM = 'Custom'


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
    slug: str
    also_appears_in: list[SmashGames]


class RosterSlot(BaseModel):
    ids: list[str]
    name: str
    slug: str
    series: Series
    availability: Availability
    also_appears_in: list[SmashGames]
    alts: list[Alt]
    variants: list[Variant]
    tips: list[Tip]
    fighters: list[Fighter]


class RosterSlotQueryParams(BaseModel):
    ids: list[str] | None = None
    names: list[str] | None = None
    series: list[Series] | None = None
    availability: list[Availability] | None = None
    also_appears_in: list[SmashGames] | None = None