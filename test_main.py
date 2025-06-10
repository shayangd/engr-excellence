from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to User Management API"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={"name": "Test User", "email": "test@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_duplicate_email():
    # First user
    client.post(
        "/api/v1/users/",
        json={"name": "User 1", "email": "duplicate@example.com"}
    )
    
    # Try to create user with same email
    response = client.post(
        "/api/v1/users/",
        json={"name": "User 2", "email": "duplicate@example.com"}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_get_nonexistent_user():
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]