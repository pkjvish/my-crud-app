###test_app.py
import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.mysql.connection')
def test_get_users(client, mock_conn):
    """Test the GET /users endpoint with mocked DB"""
    # Create a mock cursor
    mock_cur = MagicMock()
    # Set what fetchall() should return
    mock_cur.fetchall.return_value = [
        (1, "Alice", "alice@example.com"),
        (2, "Bob", "bob@example.com")
    ]
    # Link cursor to connection
    mock_conn.cursor.return_value = mock_cur

    response = client.get('/users')
    
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0][1] == "Alice"

@patch('app.mysql.connection')
def test_add_user(client, mock_conn):
    """Test the POST /users endpoint with mocked DB"""
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur

    # Payload matching the 'data' keys in app.py
    payload = {"name": "Charlie", "email": "charlie@test.com"}
    
    response = client.post('/users', json=payload)

    assert response.status_code == 201
    assert response.json == {"message": "User added successfully!"}
    # Verify DB commit was called
    mock_conn.commit.assert_called_once()

@patch('app.mysql.connection')
def test_set_db_success(client, mock_conn):
    """Test the /setdb endpoint success path"""
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur

    response = client.get('/setdb')

    assert response.status_code == 200
    assert "successfully" in response.json['message']
