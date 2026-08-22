import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_health_endpoint(client):
    rv = client.get('/health')
    assert rv.status_code == 200

def test_cache_endpoint(client):
    rv = client.get('/cache')
    assert rv.status_code == 200

def test_metrics_endpoint(client):
    rv = client.get('/metrics')
    assert rv.status_code == 200
