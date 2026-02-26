import json
from pydantic_core import ValidationError
from slugify import slugify
import pytest
from schemas.roster_slots import RosterSlot, SmashGames
from constants import ROSTER_SLOT_ALT_AMOUNT, TOTAL_ROSTER_SLOTS


data = None

with open('data/roster_slots.json', 'r') as f:
    data = json.load(f)


class TestRosterSlotDataIntegrity:
    def test_roster_slots_are_list(self):
        assert isinstance(data, list)

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_roster_slots_json_schema(self, entry):
        try:
            RosterSlot.model_validate(entry)
        except ValidationError as e:
            pytest.fail(f"Pydantic Validation failed for entry '{entry.get('name', 'Unknown')}':\n{e}")

    def test_roster_slots_json_schema_invalid(self):
        with pytest.raises(ValidationError):
            entry = data[0].copy()
            entry['invalid_extra_field'] = 'Should fail because of the "forbid extra" setting'
            RosterSlot.model_validate(entry)

        with pytest.raises(ValidationError):
            entry = data[0].copy()
            del entry['name']
            RosterSlot.model_validate(entry)

    def test_roster_slots_amount(self):
        assert len(data) == TOTAL_ROSTER_SLOTS

    def test_ids_unique_externally(self):
        all_ids = []

        for entry in data:
            all_ids.extend(entry['ids'])
            
        assert len(all_ids) == len(set(all_ids))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_ids_unique_internally(self, entry):
        assert len(entry['ids']) == len(set(entry['ids']))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_fighter_ids_unique(self, entry):
        fighter_ids = [fighter['id'] for fighter in entry['fighters']]
        assert len(fighter_ids) == len(set(fighter_ids))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_also_appears_in_unique(self, entry):
        assert len(entry['also_appears_in']) == len(set(entry['also_appears_in']))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_variant_names_unique(self, entry):
        variant_names = [v['name'] for v in entry['variants']]
        assert len(variant_names) == len(set(variant_names))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_tip_contents_unique(self, entry):
        tip_contents = [t['content'] for t in entry['tips']]
        assert len(tip_contents) == len(set(tip_contents))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_fighter_names_unique(self, entry):
        fighter_names = [fighter['name'] for fighter in entry['fighters']]
        assert len(fighter_names) == len(set(fighter_names))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_alts_ordered(self, entry):
        assert all(alt['slot'] == i for i, alt in enumerate(entry['alts'], start=1))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_roster_slot_ids_equal_fighter_ids(self, entry):
        fighter_ids = [fighter['id'] for fighter in entry['fighters']]
        assert fighter_ids == entry['ids']

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_alt_variant_mapping(self, entry):
        valid_variant_names = [v['name'] for v in entry['variants']]

        for alt in entry['alts']:
            assert alt['variant'] in valid_variant_names

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_alt_amounts(self, entry):
        assert len(entry['alts']) == ROSTER_SLOT_ALT_AMOUNT

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_slugs(self, entry):
        assert entry['slug'] == slugify(entry['name'])

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_roster_slot_and_fighters_appear_in_same_games(self, entry):
        roster_slot_games = entry['also_appears_in']
        
        for fighter in entry['fighters']:
            fighter_games = fighter['also_appears_in']

            if fighter['name'] == 'Charizard': # Charizard is the only special case where it appears in more games than Pokémon Trainer
                assert all(game in fighter_games for game in roster_slot_games)
            else:
                assert roster_slot_games == fighter_games

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_ids_ordered(self, entry):
        assert entry['ids'] == sorted(entry['ids'])

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_fighter_ids_ordered(self, entry):
        fighter_ids = [fighter['id'] for fighter in entry['fighters']]
        assert fighter_ids == sorted(fighter_ids)

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_also_appears_in_ordered(self, entry):
        games_ordered = [game.value for game in SmashGames]
        all_also_appears_in = [entry['also_appears_in']] + [fighter['also_appears_in'] for fighter in entry['fighters']]

        for also_appears_in in all_also_appears_in:
            previous_game = None

            for game in also_appears_in:
                if previous_game is None:
                    previous_game = game
                else:
                    assert games_ordered.index(previous_game) < games_ordered.index(game)

    def test_tips_are_not_empty(self):
        pytest.skip("This test will be skipped until tips are added to the JSON data.")

