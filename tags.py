from enum import StrEnum


class Tags(StrEnum):
    ROSTER_SLOTS = 'Roster Slots'
    STAGES = 'Stages'
    ITEMS = 'Items'
    FIGHTERS = 'Fighters'


TAGS_METADATA = [
    {
        'name': Tags.ROSTER_SLOTS,
        'description': '...',
    },
    {
        'name': Tags.FIGHTERS,
        'description': '...',
    },
    {
        'name': Tags.STAGES,
        'description': '...',
    },
    {
        'name': Tags.ITEMS,
        'description': '...',
    },
]
