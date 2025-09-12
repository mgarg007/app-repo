import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_healthz(client):
    """Test /healthz endpoint returns status ok"""
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_home(client):
    """Test / root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, GitOps with GitLab and FluxCD!" in response.data
