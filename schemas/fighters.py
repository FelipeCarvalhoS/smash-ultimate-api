from pydantic import BaseModel
from schemas.shared import SmashGames


class Fighter(BaseModel):
    id: str
    name: str
    slug: str
    also_appears_in: list[SmashGames]

    model_config = {'extra': 'forbid'}
    