from fastapi.testclient import TestClient
import pytest
from main import app
from schemas.fighters import Fighter


client = TestClient(app)


class TestRosterSlotRouter:
    @pytest.mark.parametrize('id, name', [
        ('25e', 'Chrom'),
        ('33', 'Squirtle'),
        ('34', 'Ivysaur'),
        ('35', 'Charizard'),
        ('79', 'Pyra'),
        ('80', 'Mythra'),
    ])
    def test_get_fighter_200(self, id, name):
        response = client.get(f'/fighters/{id}')
        assert response.status_code == 200
        data = response.json()
        assert Fighter.model_validate(data)
        assert data['name'] == name

    @pytest.mark.parametrize('id', [
        'invalid-id',
        '0',
        '83',
        '-1',
    ])
    def test_get_fighter_404(self, id):
        response = client.get(f'/fighters/{id}')
        assert response.status_code == 404

    def test_get_random_fighter(self):
        response = client.get('/fighters/random')
        assert response.status_code == 200
        data = response.json()
        assert Fighter.model_validate(data)
