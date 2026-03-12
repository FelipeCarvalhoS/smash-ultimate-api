from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestRoot:
    def test_get_root(self):
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 307
        assert response.headers['location'] == '/redoc'
