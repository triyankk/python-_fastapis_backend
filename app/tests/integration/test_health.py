from fastapi.testclient import TestClient
import pytest

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_auth_health(client: TestClient):
    response = client.get("/api/v1/auth/")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "message" in data
