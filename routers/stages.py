from fastapi import APIRouter
from fastapi.exceptions import HTTPException
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
    filter_query: Annotated[StageQueryParams, Query()]
) -> list[Stage]:
    return stage_service.filter(
        id=filter_query.ids,
        name=filter_query.names,
        series=filter_query.series,
        availability=filter_query.availability,
        also_appears_in=filter_query.also_appears_in,
        is_original_or_new_version=filter_query.is_original_or_new_version,
    )
