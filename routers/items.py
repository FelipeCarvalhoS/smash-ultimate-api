from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page
from schemas.items import Item, ItemQueryParams
from services.items import item_service
from typing import Annotated
from fastapi import Query
from random import choice
from tags import Tags


router = APIRouter(
    prefix='/items',
    tags=[Tags.ITEMS],
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
    query: Annotated[ItemQueryParams, Query()] = None,
) -> Page[Item]:
    '''
    Filter items based on the query parameters and returns them ordered by ID.
    It also does not return duplicate items.

    **How the filter works**
    - For parameters that are lists, the item needs to match at least one of the values in the list.
    - The item needs to match all the parameters provided in the query.

    **Example**: If the query is `?types=Explosive&name=Bomber&name=Food`, the item must be of type Explosive
    <u>and</u> the name must be Bomber <u>or</u> Food. In this example, only the Bomber item
    would be returned because the Food one does not match the types filter.
    '''
    return item_service.filter_and_paginate(
        ItemQueryParams(
            id=query.id,
            name=query.name,
            series=query.series,
            also_appears_in=query.also_appears_in,
            types=query.types,
            heavy=query.heavy,
        )
    )
