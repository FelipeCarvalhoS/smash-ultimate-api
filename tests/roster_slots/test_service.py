from collections import Counter
from fastapi.testclient import TestClient
from fastapi_pagination import Params, set_params
from constants import ROSTER_SLOTS_TOTAL
from main import app
from schemas.roster_slots import RosterSlotQueryParams
from services.roster_slots import roster_slot_service
import pytest
from tests.items.test_service import FILTER_PAGINATE_TEST_CASES


FILTER_TEST_CASES = [
    (RosterSlotQueryParams(ids=['26']), ['Mr. Game & Watch']),
    (RosterSlotQueryParams(ids=['1', '2', '4e']), ['Mario', 'Donkey Kong', 'Dark Samus']),
    (RosterSlotQueryParams(ids=['33', '34', '35', '79', '80']), ['Pyra/Mythra', 'Pokémon Trainer']),
    (RosterSlotQueryParams(ids=['0', '81']), ['Kazuya']),
    (RosterSlotQueryParams(ids=['invalid', '0', str(ROSTER_SLOTS_TOTAL + 1), '-1']), []),
    (RosterSlotQueryParams(name=['Dr. Mario']), ['Dr. Mario']),
    (RosterSlotQueryParams(name=['Pokémon Trainer', 'Luigi', 'invalid']), ['Luigi', 'Pokémon Trainer']),
    (RosterSlotQueryParams(series=['Metroid']), ['Samus', 'Dark Samus', 'Zero Suit Samus', 'Ridley']),
    (RosterSlotQueryParams(series=['Castlevania']), ['Simon', 'Richter']),
    (RosterSlotQueryParams(series=['Kingdom Hearts']), ['Sora']),
    (RosterSlotQueryParams(series=['Xenoblade Chronicles']), ['Pyra/Mythra', 'Shulk']),
    (RosterSlotQueryParams(availability=['Paid DLC']), ['Piranha Plant', 'Joker', 'Hero', 'Banjo & Kazooie', 'Terry', 'Byleth', 'Min Min', 'Steve', 'Sephiroth', 'Pyra/Mythra', 'Kazuya', 'Sora']),
    (RosterSlotQueryParams(availability=['Starter', 'Custom']), ['Mario', 'Donkey Kong', 'Link', 'Fox', 'Kirby', 'Pikachu', 'Samus', 'Yoshi', 'Mii Gunner', 'Mii Brawler', 'Mii Swordfighter']),
    (RosterSlotQueryParams(also_appears_in=['64']), ['Mario', 'Donkey Kong', 'Link', 'Fox', 'Kirby', 'Pikachu', 'Samus', 'Yoshi', 'Luigi', 'Ness', 'Captain Falcon', 'Jigglypuff']),
    (RosterSlotQueryParams(also_appears_in=['Melee']), ['Dr. Mario', 'Mario', 'Luigi', 'Bowser', 'Peach', 'Yoshi', 'Donkey Kong', 'Captain Falcon', 'Ganondorf', 'Falco', 'Fox', 'Ness', 'Ice Climbers', 'Kirby', 'Samus', 'Zelda', 'Sheik', 'Link', 'Young Link', 'Pichu', 'Pikachu', 'Jigglypuff', 'Mewtwo', 'Mr. Game & Watch', 'Marth', 'Roy']),
    (RosterSlotQueryParams(also_appears_in=['64', 'Melee']), ['Dr. Mario', 'Mario', 'Luigi', 'Bowser', 'Peach', 'Yoshi', 'Donkey Kong', 'Captain Falcon', 'Ganondorf', 'Falco', 'Fox', 'Ness', 'Ice Climbers', 'Kirby', 'Samus', 'Zelda', 'Sheik', 'Link', 'Young Link', 'Pichu', 'Pikachu', 'Jigglypuff', 'Mewtwo', 'Mr. Game & Watch', 'Marth', 'Roy']),
    (RosterSlotQueryParams(ids=['1', '2', '3', '4e', '18'], also_appears_in=['64']), ['Mario', 'Donkey Kong', 'Link']),
    (RosterSlotQueryParams(also_appears_in=['3DS', 'Wii U'], series=['Metroid']), ['Samus', 'Zero Suit Samus']),
    (RosterSlotQueryParams(also_appears_in=['3DS', 'Wii U'], series=['Metroid'], availability=['Unlockable']),['Zero Suit Samus']),
]


FILTER_PAGINATE_TEST_CASES = [
    (RosterSlotQueryParams(availability=['Paid DLC']), Params(page=2, size=6), ['Min Min', 'Steve', 'Sephiroth', 'Pyra/Mythra', 'Kazuya', 'Sora']),
    (RosterSlotQueryParams(also_appears_in=['64', 'Melee']), Params(page=1, size=3), ['Mario', 'Donkey Kong', 'Link']),
    (RosterSlotQueryParams(also_appears_in=['64']), Params(), ['Mario', 'Donkey Kong', 'Link', 'Samus', 'Yoshi', 'Kirby', 'Fox', 'Pikachu', 'Luigi', 'Ness', 'Captain Falcon', 'Jigglypuff']),
]


class TestRosterSlotService:
    client = TestClient(app)

    @pytest.mark.parametrize('id, name', [
        ('1', 'Mario'),
        ('2', 'Donkey Kong'),
        ('4e', 'Dark Samus'),
        ('33', 'Pokémon Trainer'),
        ('34', 'Pokémon Trainer'),
        ('35', 'Pokémon Trainer'),
        ('58', 'Bowser Jr.'),
        ('64', 'Inkling'),
        ('79', 'Pyra/Mythra'),
        ('80', 'Pyra/Mythra'),
        ('81', 'Kazuya'),
        ('82', 'Sora'),
    ]) 
    def test_get_by_id(self, id, name):
        roster_slot = roster_slot_service.get_by_id(id)
        assert id in roster_slot.ids
        assert roster_slot.name == name

    @pytest.mark.parametrize('id', ['invalid-id', '0', str(ROSTER_SLOTS_TOTAL + 1), '-1'])
    def test_get_by_id_not_found(self, id):
        roster_slot = roster_slot_service.get_by_id(id)
        assert roster_slot is None

    def test_get_all(self):
        roster_slots = roster_slot_service.get_all()
        assert len(roster_slots) == ROSTER_SLOTS_TOTAL

    @pytest.mark.parametrize('roster_slot', roster_slot_service.get_all())
    def test_ids_return_correct_roster_slot(self, roster_slot):
        for fighter_id in roster_slot.ids:
            assert roster_slot_service.get_by_id(fighter_id) == roster_slot

    @pytest.mark.parametrize('query_params, expected_names', FILTER_TEST_CASES)
    def test_filter(self, query_params, expected_names):
        roster_slots = roster_slot_service._filter(query_params)
        assert Counter([slot.name for slot in roster_slots]) == Counter(expected_names)

    @pytest.mark.parametrize('name', ['mario', 'MARIO', 'MaRiO', 'mArIo', 'maRio'])
    def test_filter_name_case_insensitivity(self, name):
        roster_slots = roster_slot_service._filter(RosterSlotQueryParams(name=[name]))
        assert roster_slots[0].name == 'Mario'

    def test_filter_does_not_return_duplicates(self):
        roster_slots = roster_slot_service._filter(RosterSlotQueryParams(ids=['33', '34', '35', '79', '80'] * 2))
        assert len(roster_slots) == len(set(roster_slot.name for roster_slot in roster_slots))

    @pytest.mark.parametrize('query_params, page_params, expected_names', FILTER_PAGINATE_TEST_CASES)
    def test_filter_and_paginate(self, query_params, page_params, expected_names):
        with set_params(page_params):
            page = roster_slot_service.filter_and_paginate(query_params)
            
        assert [roster_slot.name for roster_slot in page.items] == expected_names
