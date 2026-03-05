import json
from pydantic_core import ValidationError
from slugify import slugify
import pytest
from schemas.items import Item, SmashGames
from constants import TOTAL_ITEMS


with open('data/items.json', 'r') as f:
    data = json.load(f)


class TestItemDataIntegrity:
    def test_items_are_list(self):
        assert isinstance(data, list)

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_items_json_schema(self, entry):
        try:
            Item.model_validate(entry)
        except ValidationError as e:
            pytest.fail(f"Pydantic Validation failed for entry '{entry.get('name', 'Unknown')}':\n{e}")

    def test_items_json_schema_invalid(self):
        with pytest.raises(ValidationError):
            entry = data[0].copy()
            entry['invalid_extra_field'] = 'Should fail because of the "forbid extra" setting'
            Item.model_validate(entry)

        with pytest.raises(ValidationError):
            entry = data[0].copy()
            del entry['name']
            Item.model_validate(entry)

    def test_items_amount(self):
        assert len(data) == TOTAL_ITEMS

    def test_ids_unique(self):
        all_ids = [entry['id'] for entry in data]
        assert len(all_ids) == len(set(all_ids))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_also_appears_in_unique(self, entry):
        assert len(entry['also_appears_in']) == len(set(entry['also_appears_in']))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_slugs(self, entry):
        assert entry['slug'] == slugify(entry['name'])

    def test_slugs_unique(self):
        all_slugs = [entry['slug'] for entry in data]
        assert len(all_slugs) == len(set(all_slugs))

    @pytest.mark.parametrize('entry', data, ids=lambda x: x['slug'])
    def test_also_appears_in_ordered(self, entry):
        games_ordered = [game.value for game in SmashGames]

        previous_game = None

        for game in entry['also_appears_in']:
            if previous_game is None:
                previous_game = game
            else:
                assert games_ordered.index(previous_game) < games_ordered.index(game)

    @pytest.mark.parametrize('i, entry', enumerate(data), ids=[d['slug'] for d in data])
    def test_ids_ordered(self, i, entry):
        assert entry['id'] == i + 1
