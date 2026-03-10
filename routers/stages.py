from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page
from schemas.stages import Stage, StageQueryParams
from services.stages import stage_service
from typing import Annotated
from fastapi import Query
from random import choice


router = APIRouter(
    prefix='/stages',
    tags=['Stages'],
)
        

@router.get('/random')
async def get_random_stage() -> Stage:
    return choice(stage_service.get_all())


@router.get('/{id}', responses={404: {'description': 'Stage not found'}})
async def get_stage(id: int) -> Stage:
    stage = stage_service.get_by_id(id)

    if stage is not None:
        return stage

    raise HTTPException(status_code=404)


@router.get('')
async def filter_stages(
    query: Annotated[StageQueryParams, Query()]
) -> Page[Stage]:
    return stage_service.filter_and_paginate(
        id=query.ids,
        name=query.names,
        series=query.series,
        availability=query.availability,
        also_appears_in=query.also_appears_in,
        is_original_or_new_version=query.is_original_or_new_version,
    )
