from collections import Counter
from fastapi.testclient import TestClient
from constants import TOTAL_STAGES
from main import app
from services.stages import stage_service
import pytest


FILTER_TEST_CASES = [
    ({'id': [1, 2, 3, 114]}, ['Battlefield', 'Small Battlefield', 'Big Battlefield', 'Mishima Dojo']),
    ({'name': ['Destination']}, ['Final Destination']),
    ({'name': ['Battlefield']}, ['Battlefield', 'Small Battlefield', 'Big Battlefield']),
    ({'name': ['battleFIELD', 'DESTination']}, ['Final Destination', 'Battlefield', 'Small Battlefield', 'Big Battlefield']),
    ({'series': ['Yoshi']}, ["Yoshi's Island (Melee)", "Yoshi's Story", "Yoshi's Island", 'Super Happy Tree']),
    ({'series': ['Minecraft']}, ['Minecraft World']),
    ({'series': ['Minecraft', 'Kingdom Hearts']}, ['Minecraft World', 'Hollow Bastion']),
    ({'availability': ['Free DLC']}, ['Small Battlefield']),
    ({'is_original_or_new_version': True}, ['Battlefield', 'Big Battlefield', 'Final Destination', 'Small Battlefield']),
    ({'is_original_or_new_version': True, 'name': ['Battlefield']}, ['Small Battlefield', 'Big Battlefield', 'Battlefield']),
    ({'is_original_or_new_version': True, 'name': ['Battlefield'], 'availability': ['Starter']}, ['Big Battlefield', 'Battlefield']),
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

    @pytest.mark.parametrize('id', [0, TOTAL_STAGES + 1, -1])
    def test_get_by_id_not_found(self, id):
        stage = stage_service.get_by_id(id)
        assert stage is None

    def test_get_all(self):
        stages = stage_service.get_all()
        assert len(stages) == TOTAL_STAGES

    @pytest.mark.parametrize('stage', stage_service.get_all(), ids=lambda x: x.id)
    def test_id_returns_correct_stage(self, stage):
        assert stage_service.get_by_id(stage.id) == stage

    @pytest.mark.parametrize('filters, expected_names', FILTER_TEST_CASES)
    def test_filter(self, filters, expected_names):
        stages = stage_service.filter(**filters)
        assert Counter([stage.name for stage in stages]) == Counter(expected_names)

    @pytest.mark.parametrize('name', ['battlefield', 'BATTLEFIELD', 'Battlefield', 'bAttLefielD'])
    def test_filter_name_case_insensitivity(self, name):
        stages = stage_service.filter(name=[name])
        assert Counter([stage.name for stage in stages]) == Counter(['Battlefield', 'Big Battlefield', 'Small Battlefield'])

    def test_filter_does_not_return_duplicates(self):
        stages = stage_service.filter(id=[33, 0, TOTAL_STAGES, 1, TOTAL_STAGES + 1] * 2)
        assert len(stages) == len(set(stage.name for stage in stages))
