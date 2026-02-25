from utils.loader import load_json
from schemas.roster_slots import RosterSlot


class RosterSlotService:
    def __init__(self):
        self._data = [RosterSlot.model_validate(roster_slot) for roster_slot in load_json('roster_slots.json')]
        self._indexes = self._get_indexes()
        self._filter_strategies = {
            'ids': lambda attr, query: any(id in query for id in attr),
            'name': lambda attr, query: any(name.lower() in attr.lower() for name in query),
            'series': lambda attr, query: attr in query,
            'availability': lambda attr, query: attr in query,
            'also_appears_in': lambda attr, query: any(game in query for game in attr),
        }

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
                filter_strategy = self._filter_strategies[key]

                if not filter_strategy(attr, value):
                    matches = False
                    break

            if matches:
                filtered.append(roster_slot)

        return filtered


roster_slot_service = RosterSlotService()