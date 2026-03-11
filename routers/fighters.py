from random import choice
from fastapi import APIRouter
from routers.roster_slots import get_random_roster_slot, get_roster_slot
from schemas.roster_slots import Fighter
from tags import Tags


router = APIRouter(
    prefix='/fighters',
    tags=[Tags.FIGHTERS],
)


@router.get('/random')
async def get_random_fighter() -> Fighter:
    roster_slot = await get_random_roster_slot()
    return choice(roster_slot.fighters)


@router.get('/{id}', responses={404: {'description': 'Fighter not found'}})
async def get_fighter(id: str) -> Fighter:
    roster_slot = await get_roster_slot(id)
    return next(fighter for fighter in roster_slot.fighters if fighter.id == id)
        