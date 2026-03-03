from services.base import Service
from schemas.stages import Stage


class StageService(Service[Stage]):
    def __init__(self):
        super().__init__(Stage, 'stages.json')
    
    def _get_filter_strategies(self):
        return {
            'id': lambda attr, query: attr in query,
            'name': lambda attr, query: any(name.lower() in attr.lower() for name in query),
            'series': lambda attr, query: attr in query,
            'availability': lambda attr, query: attr in query,
            'also_appears_in': lambda attr, query: any(game in query for game in attr),
            'is_original_or_new_version': lambda attr, query: attr == query,
        }
    
    def get_by_id(self, id: int) -> Stage | None:
        if 1 <= id <= len(self._data):
            return self._data[id-1]
        
        return None


stage_service = StageService()