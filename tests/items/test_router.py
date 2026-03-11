from fastapi.testclient import TestClient
from fastapi_pagination import Page, Params, set_params
from constants import ITEMS_TOTAL
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
        response = client.get(f'/items/{str(ITEMS_TOTAL + 1)}')
        assert response.status_code == 404

    def test_get_random_item(self):
        response = client.get('/items/random')
        assert response.status_code == 200
        data = response.json()
        assert Item.model_validate(data)

    def test_filter_items(self):
        with set_params(Params()):
            response = client.get('/items?names=Poké Ball&also_appears_in=64')

        assert response.status_code == 200
        data = response.json()
        assert Page.model_validate(data)
        assert all(Item.model_validate(item) for item in data['items'])
        assert ['Poké Ball'] == [item['name'] for item in data['items']]