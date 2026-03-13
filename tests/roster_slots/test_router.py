from fastapi.testclient import TestClient
from fastapi_pagination import Page, Params, set_params
from fastapi import status
from main import app
from schemas.roster_slots import Alt, Fighter, RosterSlot, Tip, Variant


client = TestClient(app)


class TestRosterSlotRouter:
    def test_get_roster_slot_200(self):
        response = client.get('/roster-slots/66e')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert RosterSlot.model_validate(data)
        assert data['name'] == 'Richter'

    def test_get_roster_slot_404(self):
        response = client.get('/roster-slots/83')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_roster_slot_fighters_200(self):
        response = client.get('/roster-slots/13e/fighters')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert all(Fighter.model_validate(fighter) for fighter in data)
        assert data[0]['name'] == 'Daisy'

    def test_get_roster_slot_fighters_404(self):
        response = client.get('/roster-slots/0/fighters')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_roster_slot_variants_200(self):
        response = client.get('/roster-slots/58/variants')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert all(Variant.model_validate(variant) for variant in data)
        assert data[7]['name'] == 'Ludwig'

    def test_get_roster_slot_variants_404(self):
        response = client.get('/roster-slots/0/variants')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_roster_slot_alts_200(self):
        response = client.get('/roster-slots/77/alts')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert all(Alt.model_validate(alt) for alt in data)
        assert data[6]['variant'] == 'Zombie'

    def test_get_roster_slot_alts_404(self):
        response = client.get('/roster-slots/0/alts')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_roster_slot_tips_200(self):
        response = client.get('/roster-slots/80/tips')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert all(Tip.model_validate(tip) for tip in data)
        assert data[0]['title'] == "Pyra/Mythra's Origins"

    def test_get_roster_slot_tips_404(self):
        response = client.get('/roster-slots/0/tips')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_random_roster_slot(self):
        response = client.get('/roster-slots/random')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert RosterSlot.model_validate(data)

    def test_filter_roster_slots(self):
        with set_params(Params()):
            response = client.get('/roster-slots?name=Bowser Jr.')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert Page.model_validate(data)
        assert all(RosterSlot.model_validate(roster_slot) for roster_slot in data['items'])
        assert ['Bowser Jr.'] == [roster_slot['name'] for roster_slot in data['items']]