import os
# Set environment variables for testing
os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["DEBUG"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./test_alhasade.db"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "test_register@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        },
    )
    print(f"Registration response status: {response.status_code}")
    print(f"Registration response body: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_register@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    print("User registration test passed!")

def test_login_user():
    # First register a user
    client.post(
        "/auth/register",
        json={
            "email": "test_login@example.com",
            "password": "testpassword123",
            "full_name": "Test User 2"
        },
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        data={
            "username": "test_login@example.com",
            "password": "testpassword123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    print("User login test passed!")

def test_refresh_token():
    # First register and login to get tokens
    client.post(
        "/auth/register",
        json={
            "email": "test_refresh@example.com",
            "password": "testpassword123",
            "full_name": "Test User 3"
        },
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "test_refresh@example.com",
            "password": "testpassword123"
        },
    )
    print(f"Login response: {login_response.json()}")
    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]
    
    # Then refresh
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    print(f"Refresh response status: {response.status_code}")
    print(f"Refresh response body: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    print("Token refresh test passed!")

if __name__ == "__main__":
    test_register_user()
    test_login_user()
    test_refresh_token()
    print("All tests passed!")