from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from ....main import app
from ....core.security import create_access_token
from ....models.user import User

def test_register_user(client: TestClient, db: Session):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User created successfully"

    # Verify user in database
    user = db.query(User).filter(User.email == "test@example.com").first()
    assert user is not None
    assert user.username == "testuser"
    assert not user.is_active  # Should be inactive until email verification

def test_login_success(client: TestClient, test_user: dict):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None

def test_protected_route(client: TestClient, test_user: dict):
    token = create_access_token(test_user["username"])
    response = client.get(
        "/api/v1/auth/user/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user["username"]
