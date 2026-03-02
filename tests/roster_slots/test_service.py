from collections import Counter
from fastapi.testclient import TestClient
from constants import TOTAL_ROSTER_SLOTS
from main import app
from services.roster_slots import roster_slot_service
import pytest


FILTER_TEST_CASES = [
    ({'ids': ['26']}, ['Mr. Game & Watch']),
    ({'ids': ['1', '2', '4e']}, ['Mario', 'Donkey Kong', 'Dark Samus']),
    ({'ids': ['33', '34', '35', '79', '80']}, ['Pyra/Mythra', 'Pokémon Trainer']),
    ({'ids': ['0', '81']}, ['Kazuya']),
    ({'ids': ['invalid', '0', '83', '-1']}, []),
    ({'name': ['Mario']}, ['Dr. Mario', 'Mario']),
    ({'name': ['pOkÉmon TraineR']}, ['Pokémon Trainer']),
    ({'name': ['KING']}, ['King K. Rool', 'King Dedede']),
    ({'name': ['King K']}, ['King K. Rool']),
    ({'name': ['samus']}, ['Samus', 'Dark Samus', 'Zero Suit Samus']),
    ({'name': ['invalid']}, []),
    ({'series': ['Metroid']}, ['Samus', 'Dark Samus', 'Zero Suit Samus','Ridley']),
    ({'series': ['Castlevania']}, ['Simon', 'Richter']),
    ({'series': ['Kingdom Hearts']}, ['Sora']),
    ({'series': ['Xenoblade Chronicles']}, ['Pyra/Mythra', 'Shulk']),
    ({'series': ['invalid']}, []),
    ({'availability': ['DLC']}, ['Piranha Plant', 'Joker', 'Hero', 'Banjo & Kazooie', 'Terry', 'Byleth', 'Min Min', 'Steve', 'Sephiroth', 'Pyra/Mythra', 'Kazuya', 'Sora']),
    ({'availability': ['Starter', 'Custom']}, ['Mario', 'Donkey Kong', 'Link', 'Fox', 'Kirby', 'Pikachu', 'Samus', 'Yoshi', 'Mii Gunner', 'Mii Brawler', 'Mii Swordfighter']),
    ({'availability': ['invalid']}, []),
    ({'also_appears_in': ['64']}, ['Mario', 'Donkey Kong', 'Link', 'Fox', 'Kirby', 'Pikachu', 'Samus', 'Yoshi', 'Luigi', 'Ness', 'Captain Falcon', 'Jigglypuff']),
    ({'also_appears_in': ['Melee']}, ['Dr. Mario', 'Mario', 'Luigi', 'Bowser', 'Peach', 'Yoshi', 'Donkey Kong', 'Captain Falcon', 'Ganondorf', 'Falco', 'Fox', 'Ness', 'Ice Climbers', 'Kirby', 'Samus', 'Zelda', 'Sheik', 'Link', 'Young Link', 'Pichu', 'Pikachu', 'Jigglypuff', 'Mewtwo', 'Mr. Game & Watch', 'Marth', 'Roy']),
    ({'also_appears_in': ['64', 'Melee']}, ['Dr. Mario', 'Mario', 'Luigi', 'Bowser', 'Peach', 'Yoshi', 'Donkey Kong', 'Captain Falcon', 'Ganondorf', 'Falco', 'Fox', 'Ness', 'Ice Climbers', 'Kirby', 'Samus', 'Zelda', 'Sheik', 'Link', 'Young Link', 'Pichu', 'Pikachu', 'Jigglypuff', 'Mewtwo', 'Mr. Game & Watch', 'Marth', 'Roy']),
    ({'also_appears_in': ['invalid']}, []),
    ({'ids': ['1', '2', '3', '4e', '18'], 'name': ['o']}, ['Dr. Mario', 'Mario', 'Donkey Kong']),
    ({'ids': ['1', '2', '3', '4e', '18'], 'name': ['o'], 'also_appears_in': ['64']}, ['Mario', 'Donkey Kong']),
    ({'also_appears_in': ['3DS', 'Wii U'], 'series': ['Metroid']}, ['Samus', 'Zero Suit Samus']),
    ({'also_appears_in': ['3DS', 'Wii U'], 'series': ['Metroid'], 'availability': ['Unlockable']}, ['Zero Suit Samus']),
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

    @pytest.mark.parametrize('id', ['invalid-id', '0', '83', '-1'])
    def test_get_by_id_not_found(self, id):
        roster_slot = roster_slot_service.get_by_id(id)
        assert roster_slot is None

    def test_get_all(self):
        roster_slots = roster_slot_service.get_all()
        assert len(roster_slots) == TOTAL_ROSTER_SLOTS

    def test_all_ids_return_correct_slots(self):
        all_slots = roster_slot_service.get_all()
        for slot in all_slots:
            for fighter_id in slot.ids:
                assert roster_slot_service.get_by_id(fighter_id) == slot

    @pytest.mark.parametrize('filters, expected_names', FILTER_TEST_CASES)
    def test_filter(self, filters, expected_names):
        roster_slots = roster_slot_service.filter(**filters)
        assert Counter([slot.name for slot in roster_slots]) == Counter(expected_names)

    @pytest.mark.parametrize('name', ['mario', 'MARIO', 'MaRiO', 'mArIo', 'maRio'])
    def test_filter_name_case_insensitivity(self, name):
        roster_slots = roster_slot_service.filter(name=[name])
        assert Counter([slot.name for slot in roster_slots]) == Counter(['Dr. Mario', 'Mario'])

    def test_filter_does_not_return_duplicates(self):
        roster_slots = roster_slot_service.filter(ids=['33', '34', '35', '79', '80'] * 2)
        assert len(roster_slots) == len(set(roster_slot.name for roster_slot in roster_slots))
