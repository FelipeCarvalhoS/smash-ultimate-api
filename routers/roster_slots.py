from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page
from schemas.roster_slots import Alt, RosterSlot, RosterSlotQueryParams, Fighter, Tip, Variant
from services.roster_slots import roster_slot_service
from typing import Annotated
from fastapi import Query
from random import choice
from tags import Tags


router = APIRouter(
    prefix='/roster-slots',
    tags=[Tags.ROSTER_SLOTS],
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


@router.get('/{id}/variants', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_variants(id: str) -> list[Variant]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.variants


@router.get('/{id}/alts', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_alts(id: str) -> list[Alt]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.alts


@router.get('/{id}/tips', responses={404: {'description': 'Roster slot not found'}})
async def get_roster_slot_tips(id: str) -> list[Tip]:
    roster_slot = await get_roster_slot(id)
    return roster_slot.tips


@router.get('')
async def filter_roster_slots(
    query: Annotated[RosterSlotQueryParams, Query()]
) -> Page[RosterSlot]:
    '''
    Filter roster slots based on the query parameters and returns them ordered by ID.
    It also does not return duplicate roster slots.

    **How the filter works**
    - For parameters that are lists, the roster slot needs to match at least one of the values in the list.
    - The roster slot needs to match all the parameters provided in the query.

    **Example**: If the query is `?series=Mario&name=Luigi&name=Link`, the roster slot series must be Mario
    <u>and</u> the name must be Luigi <u>or</u> Link. In this example, only the Luigi roster slot
    would be returned because the Link one does not match the series filter.
    '''
    return roster_slot_service.filter_and_paginate(
        ids=query.ids,
        name=query.names,
        series=query.series,
        availability=query.availability,
        also_appears_in=query.also_appears_in,
    )
