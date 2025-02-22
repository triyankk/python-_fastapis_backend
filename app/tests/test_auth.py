from fastapi.testclient import TestClient
import pytest
from ..core.security import create_access_token

def test_register(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpass123"
        }
    )
    assert response.status_code == 200
    assert "message" in response.json()

def test_login(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_get_user_me(client: TestClient, test_user):
    access_token = create_access_token(test_user["username"])
    response = client.get(
        "/api/v1/auth/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]
