import pytest
import sys
import os
import importlib.util
from unittest.mock import MagicMock, patch

# Mock psycopg before importing app
mock_psycopg = MagicMock()
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_conn.cursor.return_value = mock_cursor
mock_cursor.fetchall.return_value = []
mock_cursor.fetchone.return_value = None
mock_psycopg.connect.return_value = mock_conn

with patch.dict('sys.modules', {'psycopg': mock_psycopg, 'psycopg2': mock_psycopg}):
    spec = importlib.util.spec_from_file_location("app", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "day9-flask", "app.py"))
    app_module = importlib.util.module_from_spec(spec)
    sys.modules["app"] = app_module
    spec.loader.exec_module(app_module)
    app = app_module.app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
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
