from fastapi.testclient import TestClient
from main import app
from schemas.roster_slots import RosterSlot


client = TestClient(app)


class TestRosterSlotRouter:
    def test_get_roster_slot_200(self):
        response = client.get('/roster-slots/66e')
        assert response.status_code == 200
        data = response.json()
        assert RosterSlot.model_validate(data)
        assert data['name'] == 'Richter'

    def test_get_roster_slot_404(self):
        response = client.get('/roster-slots/83')
        assert response.status_code == 404

    def test_get_random_roster_slot(self):
        response = client.get('/roster-slots/random')
        assert response.status_code == 200
        data = response.json()
        assert RosterSlot.model_validate(data)

    def test_filter_roster_slots(self):
        response = client.get('/roster-slots?names=Bowser')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(RosterSlot.model_validate(item) for item in data)
        assert all('Bowser' in roster_slot['name'] for roster_slot in data)