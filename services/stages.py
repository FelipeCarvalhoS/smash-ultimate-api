from services.base import Service
from utils.loader import load_json
from schemas.stages import Stage


class StageService(Service[Stage]):
    def __init__(self):
        super().__init__(Stage, 'stages.json')

    def _get_indexes(self):
        return {stage.slug: i for i, stage in enumerate(self._data)}
    
    def _get_filter_strategies(self):
        return {
            'name': lambda attr, query: any(name.lower() in attr.lower() for name in query),
            'series': lambda attr, query: attr in query,
            'availability': lambda attr, query: attr in query,
            'also_appears_in': lambda attr, query: any(game in query for game in attr),
        }
    
    def get_by_slug(self, slug: str) -> Stage | None:
        if slug in self._indexes:
            index = self._indexes[slug]
            return self._data[index]
        
        return None


stage_service = StageService()