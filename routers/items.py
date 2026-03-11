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
    query: Annotated[ItemQueryParams, Query()]
) -> Page[Item]:
    return item_service.filter_and_paginate(
        id=query.ids,
        name=query.names,
        series=query.series,
        also_appears_in=query.also_appears_in,
        types=query.types,
        heavy=query.heavy,
    )
