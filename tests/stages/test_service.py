from collections import Counter
from fastapi.testclient import TestClient
from fastapi_pagination import Params, set_params
from constants import STAGES_TOTAL
from main import app
from schemas.stages import StageQueryParams
from services.stages import stage_service
import pytest


FILTER_TEST_CASES = [
    (StageQueryParams(id=[1, 2, 3, 114]), ['Battlefield', 'Small Battlefield', 'Big Battlefield', 'Mishima Dojo']),
    (StageQueryParams(name=['Battlefield']), ['Battlefield']),
    (StageQueryParams(series=['Yoshi']), ["Yoshi's Island (Melee)", "Yoshi's Story", "Yoshi's Island", 'Super Happy Tree']),
    (StageQueryParams(series=['Minecraft']), ['Minecraft World']),
    (StageQueryParams(series=['Minecraft', 'Kingdom Hearts']), ['Minecraft World', 'Hollow Bastion']),
    (StageQueryParams(availability=['Free DLC']), ['Small Battlefield']),
    (StageQueryParams(is_original_or_new_version=True), ['Battlefield', 'Big Battlefield', 'Final Destination', 'Small Battlefield']),
    (StageQueryParams(is_original_or_new_version=True, name=['Small Battlefield', 'Big Battlefield', 'Battlefield'], availability=['Starter']), ['Big Battlefield', 'Battlefield']),
]

FILTER_PAGINATE_TEST_CASES = [
    (StageQueryParams(id=[1, 2, 3, 114]), Params(page=2, size=3), ['Mishima Dojo']),
    (StageQueryParams(name=['Final Destination']), Params(), ['Final Destination']),
    (StageQueryParams(name=['Small Battlefield', 'Big Battlefield', 'Battlefield']), Params(page=1, size=3), ['Battlefield', 'Small Battlefield', 'Big Battlefield']),
    (StageQueryParams(availability=['Free DLC']), Params(page=2, size=1), []),
]


class TestStageService:
    client = TestClient(app)

    @pytest.mark.parametrize('id, name', [
        (1, 'Battlefield'),
        (2, 'Small Battlefield'),
        (3, 'Big Battlefield'),
        (4, 'Final Destination'),
        (19, "Yoshi's Island (Melee)"),
        (20, "Yoshi's Story"),
        (38, "Yoshi's Island"),
        (101, "New Donk City Hall"),
        (106, "Yggdrasil's Altar"),
        (115, 'Hollow Bastion'),
    ]) 
    def test_get_by_id(self, id, name):
        assert stage_service.get_by_id(id).name == name

    @pytest.mark.parametrize('id', [0, STAGES_TOTAL + 1, -1])
    def test_get_by_id_not_found(self, id):
        stage = stage_service.get_by_id(id)
        assert stage is None

    def test_get_all(self):
        stages = stage_service.get_all()
        assert len(stages) == STAGES_TOTAL

    @pytest.mark.parametrize('stage', stage_service.get_all(), ids=lambda x: x.id)
    def test_id_returns_correct_stage(self, stage):
        assert stage_service.get_by_id(stage.id) == stage

    @pytest.mark.parametrize('query_params, expected_names', FILTER_TEST_CASES)
    def test_filter(self, query_params, expected_names):
        stages = stage_service._filter(query_params)
        assert Counter([stage.name for stage in stages]) == Counter(expected_names)

    @pytest.mark.parametrize('name', ['battlefield', 'BATTLEFIELD', 'Battlefield', 'bAttLefielD'])
    def test_filter_name_case_insensitivity(self, name):
        stages = stage_service._filter(StageQueryParams(name=[name]))
        assert stages[0].name == 'Battlefield'

    def test_filter_does_not_return_duplicates(self):
        stages = stage_service._filter(StageQueryParams(id=[33, 0, STAGES_TOTAL, 1, STAGES_TOTAL + 1] * 2))
        assert len(stages) == len(set(stage.name for stage in stages))

    @pytest.mark.parametrize('query_params, page_params, expected_names', FILTER_PAGINATE_TEST_CASES)
    def test_filter_and_paginate(self, query_params, page_params, expected_names):
        with set_params(page_params):
            page = stage_service.filter_and_paginate(query_params)
            
        assert [stage.name for stage in page.items] == expected_names
