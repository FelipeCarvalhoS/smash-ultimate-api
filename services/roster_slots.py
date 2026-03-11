from services.base import Service
from schemas.roster_slots import RosterSlot


class RosterSlotService(Service[RosterSlot]):
    def __init__(self):
        super().__init__(RosterSlot, 'roster_slots.json')
        self._indexes = self._get_indexes()

    def _get_indexes(self):
        indexes = {}

        for i, roster_slot in enumerate(self._data):
            for fighter in roster_slot.fighters:
                indexes[fighter.id] = i

        return indexes
    
    def _get_filter_strategies(self):
        return {
            'ids': lambda attr, query: any(id in query for id in attr),
            'name': lambda attr, query: attr.lower() in [name.lower() for name in query],
            'series': lambda attr, query: attr in query,
            'availability': lambda attr, query: attr in query,
            'also_appears_in': lambda attr, query: any(game in query for game in attr),
        }

    def get_by_id(self, id: str) -> RosterSlot | None:
        if id in self._indexes:
            index = self._indexes[id]
            return self._data[index]
        
        return None
    

roster_slot_service = RosterSlotService()