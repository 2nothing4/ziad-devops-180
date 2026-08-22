import sys
from unittest.mock import MagicMock
from importlib.machinery import SourceFileLoader

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

# Now load the app
app = SourceFileLoader("app", "day9-flask/app.py").load_module().app

import pytest

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

# Note: /cache endpoint requires Redis connection — tested locally
# CI environment runs without Redis service
