from enum import StrEnum
from utils import get_snippet


class Tags(StrEnum):
    ROSTER_SLOTS = 'Roster Slots'
    STAGES = 'Stages'
    ITEMS = 'Items'
    FIGHTERS = 'Fighters'


TAGS_METADATA = [
    {
        'name': Tags.ROSTER_SLOTS,
        'description': get_snippet('roster-slots-tag-description'),
    },
    {
        'name': Tags.FIGHTERS,
        'description': get_snippet('fighters-tag-description'),
    },
    {
        'name': Tags.STAGES,
        'description': get_snippet('stages-tag-description'),
    },
    {
        'name': Tags.ITEMS,
        'description': get_snippet('items-tag-description'),
    },
]
