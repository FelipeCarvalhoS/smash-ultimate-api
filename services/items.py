from services.base import Service
from schemas.items import Item


class ItemService(Service[Item]):
    def __init__(self):
        super().__init__(Item, 'items.json')
    
    def _get_filter_strategies(self):
        return {
            'id': lambda attr, query: attr in query,
            'name': lambda attr, query: attr.lower() in [name.lower() for name in query],
            'series': lambda attr, query: attr in query,
            'also_appears_in': lambda attr, query: any(game in query for game in attr),
            'types': lambda attr, query: any(item_type in query for item_type in attr),
            'heavy': lambda attr, query: attr == query,
        }
    
    def get_by_id(self, id: int) -> Item | None:
        if 1 <= id <= len(self._data):
            return self._data[id-1]
        
        return None


item_service = ItemService()