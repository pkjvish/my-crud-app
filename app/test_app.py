# test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_users(client):
    """Test the GET /users endpoint"""
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json == {"users": []}

def test_add_user(client):
    """Test the POST /users endpoint"""
    response = client.post('/users')
    assert response.status_code == 201
    assert response.json == {"message": "User added"}
