import sys
from unittest.mock import MagicMock
from importlib.machinery import SourceFileLoader
import pytest

# Mock psycopg before importing app
mock_psycopg = MagicMock()
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_conn.cursor.return_value = mock_cursor
mock_cursor.fetchall.return_value = []
mock_cursor.fetchone.return_value = None
mock_psycopg.connect.return_value = mock_conn

sys.modules['psycopg'] = mock_psycopg
sys.modules['psycopg2'] = mock_psycopg

# Mock Redis (cache endpoint needs it)
mock_redis = MagicMock()
mock_redis_client = MagicMock()
mock_redis_client.get.return_value = None
mock_redis_client.set.return_value = True
mock_redis.Redis.return_value = mock_redis_client
sys.modules['redis'] = mock_redis

# Now load the app (Fixed the load_module typo here)
app_module = SourceFileLoader("app", "day9-flask/app.py").load_module()
app = app_module.app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    rv = client.get('/health')
    assert rv.status_code == 200

def test_metrics_endpoint(client):
    rv = client.get('/metrics')
    assert rv.status_code == 200

# --- NEW TESTS FOR DAY 38 ---

def test_cache_endpoint_success(client, monkeypatch):
    redis_client = MagicMock()
    redis_client.get.return_value = "Day 24: Deployed on Render"
    
    monkeypatch.setattr(
        app_module,
        "get_redis_connection",
        lambda: redis_client
    )
    
    response = client.get("/cache")
    assert response.status_code == 200
    data = response.get_json()
    
    assert data == {
        "cache": "connected",
        "value": "Day 24: Deployed on Render",
        "status": "Redis caching works"
    }
    
    redis_client.set.assert_called_once_with(
        "last_visit",
        "Day 24: Deployed on Render"
    )
    redis_client.get.assert_called_once_with("last_visit")

def test_cache_endpoint_redis_failure(client, monkeypatch):
    def raise_redis_error():
        raise ConnectionError("Simulated Redis outage")
        
    monkeypatch.setattr(
        app_module,
        "get_redis_connection",
        raise_redis_error
    )
    
    response = client.get("/cache")
    assert response.status_code == 500
    assert response.get_json() == {"cache": "error", "status": "Redis connection failed"}