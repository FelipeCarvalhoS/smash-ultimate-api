from fastapi.testclient import TestClient
from fastapi_pagination import Page, Params, set_params
from constants import STAGES_TOTAL
from main import app
from schemas.stages import Stage
from fastapi import status


client = TestClient(app)


class TestStageRouter:
    def test_get_stage_200(self):
        response = client.get('/stages/102')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert Stage.model_validate(data)
        assert data['name'] == 'Great Plateau Tower'

    def test_get_stage_404(self):
        response = client.get(f'/stages/{str(STAGES_TOTAL + 1)}')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_random_stage(self):
        response = client.get('/stages/random')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert Stage.model_validate(data)

    def test_filter_stages(self):
        with set_params(Params()):
            response = client.get("/stages?name=Yoshi's Island (Melee)")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert Page.model_validate(data)
        assert all(Stage.model_validate(stage) for stage in data['items'])
        assert ["Yoshi's Island (Melee)"] == [stage['name'] for stage in data['items']]