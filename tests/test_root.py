from fastapi.testclient import TestClient
from main import app
from fastapi import status


client = TestClient(app)


class TestRoot:
    def test_get_root(self):
        response = client.get(app.root_path, follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers['location'] == app.root_path + '/redoc'
