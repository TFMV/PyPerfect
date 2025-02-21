# tests/test_health.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

status_code = 200

def test_health_check():
    response = client.get("/health")
    assert response.status_code == status_code
    assert response.json() == {"status": "OK"}
