from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestRoot:
    def test_get_root(self):
        response = client.get('/', follow_redirects=False)
        assert response.headers['location'] == app.root_path + '/redoc'
