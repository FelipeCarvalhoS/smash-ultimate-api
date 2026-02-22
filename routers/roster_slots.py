from fastapi import APIRouter
import json
from fastapi.exceptions import HTTPException
from models.roster_slots import RosterSlot


ROSTER_SLOTS: list[dict] = []

with open('data/roster_slots.json', 'r') as f:
    ROSTER_SLOTS = json.load(f)


router = APIRouter(
    prefix='/roster-slots',
    tags=['Roster Slots'],
)


@router.get('/{id}', responses={404: {"description": "Not Found"}})
async def get_roster_slot(id: str) -> RosterSlot:
    for roster_slot in ROSTER_SLOTS:
        if id in roster_slot['ids']:
            return RosterSlot(**roster_slot)
        
    raise HTTPException(status_code=404)