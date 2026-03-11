from collections import Counter
from fastapi.testclient import TestClient
from fastapi_pagination import Params, resolve_params, set_params
from constants import TOTAL_ITEMS
from main import app
from services.items import item_service
import pytest


FILTER_TEST_CASES = [
    ({'id': [1, 5, 6]}, ['Smash Ball', 'Dragoon', 'Daybreak']),
    ({'name': ['Smash Ball']}, ['Smash Ball', 'Fake Smash Ball']),
    ({'name': ['Ball'], 'series': ['Pokémon', 'Mario']}, ['Soccer Ball', 'Poké Ball', 'Master Ball']),
    ({'series': ['Clu Clu Land']}, ['Unira']),
    ({'name': ['Ball'], 'also_appears_in': ['64']}, ['Poké Ball']),
    ({'types': ['Transformation', 'Summoning']}, ['Poké Ball', 'Master Ball', 'Assist Trophy', 'Bullet Bill']),
    ({'types': ['Transformation', 'Summoning'], 'heavy': False}, ['Poké Ball', 'Master Ball', 'Assist Trophy', 'Bullet Bill']),
    ({'types': ['Transformation', 'Summoning'], 'heavy': False, 'name': ['BulLeT', 'trOPHy']}, ['Assist Trophy', 'Bullet Bill']),
    ({'types': ['Transformation', 'Summoning'], 'heavy': True}, []),
    ({'heavy': True}, ['Party Ball', 'Crate', 'Rolling Crate', 'Barrel', 'Blast Box'])
]

FILTER_PAGINATE_TEST_CASES = [
    ({'id': [1, 5, 6]}, Params(page=1, size=2), ['Smash Ball', 'Dragoon']),
    ({'id': [1, 5, 6]}, Params(page=2, size=2), ['Daybreak']),
    ({'name': ['Ball'], 'series': ['Pokémon', 'Mario']}, Params(page=1, size=10), ['Poké Ball', 'Master Ball', 'Soccer Ball']),
    ({'series': ['Clu Clu Land']}, Params(), ['Unira']),
    ({'types': ['Transformation', 'Summoning']}, Params(page=4, size=1), ['Bullet Bill']),
]


class TestItemService:
    client = TestClient(app)

    @pytest.mark.parametrize('id, name', [
        (1, 'Smash Ball'),
        (5, 'Dragoon'),
        (6, 'Daybreak'),
        (9, 'Fake Smash Ball'),
        (45, "Ramblin' Evil Mushroom"),
        (48, 'Motion-Sensor Bomb'),
        (87, 'Grass'),
    ]) 
    def test_get_by_id(self, id, name):
        assert item_service.get_by_id(id).name == name

    @pytest.mark.parametrize('id', [0, TOTAL_ITEMS + 1, -1])
    def test_get_by_id_not_found(self, id):
        item = item_service.get_by_id(id)
        assert item is None

    def test_get_all(self):
        items = item_service.get_all()
        assert len(items) == TOTAL_ITEMS

    @pytest.mark.parametrize('item', item_service.get_all(), ids=lambda x: x.id)
    def test_id_returns_correct_item(self, item):
        assert item_service.get_by_id(item.id) == item

    @pytest.mark.parametrize('filters, expected_names', FILTER_TEST_CASES)
    def test_filter(self, filters, expected_names):
        items = item_service._filter(**filters)
        assert Counter([item.name for item in items]) == Counter(expected_names)

    @pytest.mark.parametrize('name', ['Smash Ball', 'SMASH BALL', 'SmaSh baLl', 'smash ball'])
    def test_filter_name_case_insensitivity(self, name):
        items = item_service._filter(name=[name])
        assert Counter([item.name for item in items]) == Counter(['Smash Ball', 'Fake Smash Ball'])

    def test_filter_does_not_return_duplicates(self):
        items = item_service._filter(id=[33, 0, TOTAL_ITEMS, 1, TOTAL_ITEMS + 1] * 2)
        assert len(items) == len(set(item.name for item in items))

    @pytest.mark.parametrize('filters, page_params, expected_names', FILTER_PAGINATE_TEST_CASES)
    def test_filter_and_paginate(self, filters, page_params, expected_names):
        with set_params(page_params):
            page = item_service.filter_and_paginate(**filters)
            
        assert [item.name for item in page.items] == expected_names
