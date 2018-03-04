import unittest
from flask import json
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from tests.test_setup import TestSetUp


class UserAuthClass(TestSetUp):
    """
    Test user registration and login.
    """
    def test_user_can_register(self):
        """Test new user can be added to the system."""
        response = self.app.post("/api/auth/register",
                                    data=json.dumps(dict(username="testuser",
                                                    password="testpasd")),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data)
        self.assertIn("Testuser", response_msg["Message"])

    def test_blank_username(self):
        """Tests error raised with username missing."""
        response = self.app.post("/api/auth/register",
                                    data=json.dumps(dict(username="",
                                                    password="testpass")),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data)
        self.assertIn("required", response_msg["Message"])

    def test_missing_password(self):
        """Tests error raised when password is missing."""
        response = self.app.post("/api/auth/register",
                                    data=json.dumps(dict(username="testuser",
                                                    password="")),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data)
        self.assertIn("required", response_msg["Message"])

    def test_duplicate_users(self):
        """
        Tests for duplicate usernames
        """
        response = self.app.post("/api/auth/register",
                                    data=json.dumps(dict(username="testuser",
                                                    password="testpass")),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data)
        self.assertIn("already exists", response_msg["Message"])

    def test_valid_login_generates_token(self):
        """Tests token is generated on successful login."""
        response = self.app.post("/api/auth/login",
                                    data=json.dumps(dict(username="testuser",
                                                    password="testpass")),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data)
        self.assertIn("Token", response_msg)

    def test_invalid_username_login(self):
        """Tests unauthorized error raised with invalid username."""
        response = self.app.post("/api/auth/login",
                                    data=json.dumps(dict(username="invalid",
                                                    password="testpass")),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data)
        self.assertIn("Invalid", response_msg["Message"])

    def test_invalid_password_login(self):
        """Tests unauthorized error raised with invalid password."""
        response = self.app.post("/api/auth/login",
                                    data=json.dumps(dict(username="testuser",
                                                    password="invalid")),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data)
        self.assertIn("Invalid", response_msg["Message"])


if __name__ == '__main__':
    unittest.main()
