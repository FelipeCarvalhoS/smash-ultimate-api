from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from schemas.roster_slots import RosterSlot
from services.roster_slots import RosterSlotService


router = APIRouter(
    prefix='/roster-slots',
    tags=['Roster Slots'],
    responses={404: {"description": "Not Found"}},
)


@router.get('/{id}')
async def get_roster_slot(id: str) -> RosterSlot:
    roster_slot = RosterSlotService.get_by_id(id)

    if roster_slot is not None:
        return roster_slot

    raise HTTPException(status_code=404)