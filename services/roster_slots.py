from utils.loader import load_json
from schemas.roster_slots import RosterSlot


class RosterSlotService:
    _data = load_json('roster_slots.json')

    @classmethod
    def get_all(cls) -> list[RosterSlot]:
        return [RosterSlot(**roster_slot) for roster_slot in cls._data]

    @classmethod
    def get_by_id(cls, id: str) -> RosterSlot | None:
        for roster_slot in cls._data:
            if id in roster_slot['ids']:
                return RosterSlot(**roster_slot)
        
        return None
