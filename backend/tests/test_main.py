from datetime import timedelta

from fastapi.testclient import TestClient
from jose import jwt

from app.main import ALGORITHM, SECRET_KEY, app, create_access_token

client = TestClient(app)


def test_login_success():
    response = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    response = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_invalid_username():
    response = client.post("/login", json={"username": "wrong", "password": "admin123"})
    assert response.status_code == 401


def test_token_has_correct_expiration():
    response = client.post("/login", json={"username": "admin", "password": "admin123"})
    token = response.json()["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload
    assert payload["sub"] == "admin"


def test_refresh_token_success():
    login_response = client.post("/login", json={"username": "admin", "password": "admin123"})
    token = login_response.json()["access_token"]

    refresh_response = client.post("/refresh", json={"token": token})
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    # Verify the refreshed token is valid
    payload = jwt.decode(data["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "admin"


def test_refresh_token_invalid():
    response = client.post("/refresh", json={"token": "invalid.token.value"})
    assert response.status_code == 401


def test_refresh_token_expired():
    expired_token = create_access_token(
        data={"sub": "admin"}, expires_delta=timedelta(seconds=-1)
    )
    response = client.post("/refresh", json={"token": expired_token})
    assert response.status_code == 401
