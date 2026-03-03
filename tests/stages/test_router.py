from fastapi.testclient import TestClient
from main import app
from schemas.stages import Stage


client = TestClient(app)


class TestStageRouter:
    def test_get_stage_200(self):
        response = client.get('/stages/102')
        assert response.status_code == 200
        data = response.json()
        assert Stage.model_validate(data)
        assert data['name'] == 'Great Plateau Tower'

    def test_get_stage_404(self):
        response = client.get('/stages/116')
        assert response.status_code == 404

    def test_get_random_stage(self):
        response = client.get('/stages/random')
        assert response.status_code == 200
        data = response.json()
        assert Stage.model_validate(data)

    def test_filter_stages(self):
        response = client.get('/stages?names=Yoshi&names=Battlefield')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(Stage.model_validate(stage) for stage in data)
        stages = [
            'Battlefield',
            'Small Battlefield',
            'Big Battlefield',
            "Yoshi's Island (Melee)",
            "Yoshi's Story",
            "Yoshi's Island",
        ]
        assert stages == [stage['name'] for stage in data]