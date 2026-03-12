from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page
from schemas.stages import Stage, StageQueryParams
from services.stages import stage_service
from typing import Annotated
from fastapi import Query
from random import choice
from tags import Tags


router = APIRouter(
    prefix='/stages',
    tags=[Tags.STAGES],
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
    query: Annotated[StageQueryParams, Query()] = None,
) -> Page[Stage]:
    '''
    Filter stages based on the query parameters and returns them ordered by ID.
    It also does not return duplicate stages.

    **How the filter works**
    - For parameters that are lists, the stage needs to match at least one of the values in the list.
    - The stage needs to match all the parameters provided in the query.

    **Example**: If the query is `?availability=Starter&name=Battlefield&name=Mementos`, the stage availability must be Starter
    <u>and</u> the name must be Battlefield <u>or</u> Mementos. In this example, only the Battlefield stage
    would be returned because the Mementos one does not match the availability filter.
    '''
    return stage_service.filter_and_paginate(
        StageQueryParams(
            id=query.id,
            name=query.name,
            series=query.series,
            availability=query.availability,
            also_appears_in=query.also_appears_in,
            is_original_or_new_version=query.is_original_or_new_version,
        )
    )
