from utils.loader import load_json
from schemas.roster_slots import RosterSlot


class RosterSlotService:
    def __init__(self):
        self._data = [RosterSlot(**roster_slot) for roster_slot in load_json('roster_slots.json')]
        self._indexes = self._get_indexes()

    def _get_indexes(self):
        indexes = {}

        for i, roster_slot in enumerate(self._data):
            for fighter in roster_slot.fighters:
                indexes[fighter.id] = i

        return indexes

    def get_all(self) -> list[RosterSlot]:
        return self._data

    def get_by_id(self, id: str) -> RosterSlot | None:
        if id in self._indexes:
            index = self._indexes[id]
            return self._data[index]
        
        return None
    
    def filter(self, **kwargs) -> list[RosterSlot]:
        filtered = []

        for roster_slot in self._data:
            matches = True

            for key, value in kwargs.items():
                if value is None:
                    continue

                attr = getattr(roster_slot, key)

                if isinstance(value, str):
                    if value.lower() not in attr.lower():
                        matches = False
                        break

                elif isinstance(attr, list):
                    if not any(item in value for item in attr):
                        matches = False
                        break

                elif attr not in value:
                    matches = False
                    break

            if matches:
                filtered.append(roster_slot)

        return filtered


roster_slot_service = RosterSlotService()