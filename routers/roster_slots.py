from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from schemas.roster_slots import RosterSlot, SmashGames, Series
from services.roster_slots import roster_slot_service
from schemas.roster_slots import Availability
from typing import Annotated
from fastapi import Query


router = APIRouter(
    prefix='/roster-slots',
    tags=['Roster Slots'],
    responses={404: {'description': 'Not Found'}},
)


@router.get('')
async def filter_roster_slots(
    ids: Annotated[list[str] | None, Query()] = None,
    name: Annotated[str | None, Query()] = None,
    series: Annotated[list[Series] | None, Query()] = None,
    availability: Annotated[list[Availability] | None, Query()] = None,
    also_appears_in: Annotated[list[SmashGames] | None, Query()] = None,
) -> list[RosterSlot]:
    return roster_slot_service.filter(
        ids=ids,
        name=name,
        series=series,
        availability=availability,
        also_appears_in=also_appears_in,
    )
        

@router.get('/{id}')
async def get_roster_slot(id: str) -> RosterSlot:
    roster_slot = roster_slot_service.get_by_id(id)

    if roster_slot is not None:
        return roster_slot

    raise HTTPException(status_code=404)
