#test_app.py
import unittest
from unittest.mock import MagicMock, patch

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    @patch('app.mysql')
    def test_add_user_calls_db_and_returns_201(self, mock_mysql):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_mysql.connection = mock_conn

        payload = {'name': 'Alice', 'email': 'alice@example.com'}
        response = self.client.post('/users', json=payload)

        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO tbl_user(user_name, user_email) VALUES (%s, %s)",
            (payload['name'], payload['email'])
        )
        mock_conn.commit.assert_called_once()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "User added successfully!"})

    @patch('app.mysql')
    def test_get_users_returns_rows_from_db(self, mock_mysql):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        expected_rows = [
            {'user_id': 1, 'user_name': 'Alice', 'user_email': 'alice@example.com'}
        ]
        mock_cursor.fetchall.return_value = expected_rows
        mock_conn.cursor.return_value = mock_cursor
        mock_mysql.connection = mock_conn

        response = self.client.get('/users')

        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM tbl_user")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_rows)


if __name__ == '__main__':
    unittest.main()
