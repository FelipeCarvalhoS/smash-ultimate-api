from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from schemas.roster_slots import Alt, RosterSlot, RosterSlotQueryParams, Fighter, Variant
from services.roster_slots import roster_slot_service
from typing import Annotated
from fastapi import Query
from random import choice


router = APIRouter(
    prefix='/roster-slots',
    tags=['Roster Slots'],
)


@router.get('')
async def filter_roster_slots(
    filter_query: Annotated[RosterSlotQueryParams, Query()]
) -> list[RosterSlot]:
    return roster_slot_service.filter(
        ids=filter_query.ids,
        name=filter_query.names,
        series=filter_query.series,
        availability=filter_query.availability,
        also_appears_in=filter_query.also_appears_in,
    )
        

@router.get('/random')
async def get_random_roster_slot() -> RosterSlot:
    return choice(roster_slot_service.get_all())


@router.get('/{id}', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot(id: str) -> RosterSlot:
    roster_slot = roster_slot_service.get_by_id(id)

    if roster_slot is not None:
        return roster_slot

    raise HTTPException(status_code=404)


@router.get('/{id}/fighters', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_fighters(id: str) -> list[Fighter]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.fighters


@router.get('/{id}/fighters/{fighter_id}', responses={404: {'description': 'Roster slot or fighter from roster slot not found'}})
async def get_roster_slot_fighter(id: str, fighter_id: str) -> Fighter:
    roster_slot = await get_roster_slot(id)

    for fighter in roster_slot.fighters:
        if fighter.id == fighter_id:
            return fighter
        
    raise HTTPException(status_code=404)


@router.get('/{id}/variants', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_variants(id: str) -> list[Variant]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.variants


@router.get('/{id}/alts', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_alts(id: str) -> list[Alt]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.alts


@router.get('/{id}/fighters', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_fighters(id: str) -> list[Fighter]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.fighters


@router.get('/{id}/fighters/{fighter_id}', responses={404: {'description': 'Roster slot or fighter from roster slot not found'}})
async def get_roster_slot_fighter(id: str, fighter_id: str) -> Fighter:
    roster_slot = await get_roster_slot(id)

    for fighter in roster_slot.fighters:
        if fighter.id == fighter_id:
            return fighter
        
    raise HTTPException(status_code=404)


@router.get('/{id}/variants', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_variants(id: str) -> list[Variant]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.variants


@router.get('/{id}/alts', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_alts(id: str) -> list[Alt]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.alts
