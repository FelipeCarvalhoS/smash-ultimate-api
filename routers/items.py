from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from schemas.items import Item, ItemQueryParams
from services.items import item_service
from typing import Annotated
from fastapi import Query
from random import choice


router = APIRouter(
    prefix='/items',
    tags=['Items'],
)
        

@router.get('/random')
async def get_random_item() -> Item:
    return choice(item_service.get_all())


@router.get('/{id}', responses={404: {'description': 'Item not found'}})
async def get_item(id: int) -> Item:
    item = item_service.get_by_id(id)

    if item is not None:
        return item

    raise HTTPException(status_code=404)


@router.get('')
async def filter_items(
    filter_query: Annotated[ItemQueryParams, Query()]
) -> list[Item]:
    return item_service.filter(
        id=filter_query.ids,
        name=filter_query.names,
        series=filter_query.series,
        also_appears_in=filter_query.also_appears_in,
        types=filter_query.types,
        heavy=filter_query.heavy,
    )
