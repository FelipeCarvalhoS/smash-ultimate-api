from fastapi.testclient import TestClient
from constants import TOTAL_ITEMS
from main import app
from schemas.items import Item


client = TestClient(app)


class TestItemRouter:
    def test_get_item_200(self):
        response = client.get('/items/80')
        assert response.status_code == 200
        data = response.json()
        assert Item.model_validate(data)
        assert data['name'] == 'Super Launch Star'

    def test_get_item_404(self):
        response = client.get(f'/items/{str(TOTAL_ITEMS + 1)}')
        assert response.status_code == 404

    def test_get_random_item(self):
        response = client.get('/items/random')
        assert response.status_code == 200
        data = response.json()
        assert Item.model_validate(data)

    def test_filter_items(self):
        response = client.get('/items?names=Ball&also_appears_in=64')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(Item.model_validate(item) for item in data)
        items = ['Poké Ball']
        assert items == [item['name'] for item in data]