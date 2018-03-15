import unittest
import json
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from tests.setup import TestSetUp
from src.views import user_object


class UserAuthClass(TestSetUp):
    """
    Test user registration and login.
    """

    def test_user_can_register(self):
        """Test new user can be added to the system."""
        response = self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(
                dict(
                    username="testusername",
                    password="testpassword")),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("registered", response_msg["Message"])

    def test_blank_username(self):
        """Tests error raised with username missing."""
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(username="",
                                                      password="testpass")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_missing_password(self):
        """Tests error raised when password is missing."""
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(username="testusername",
                                                      password="")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_duplicate_users(self):
        """
        Tests for duplicate usernames
        """
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(username="testuser",
                                                      password="password")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])

    def test_valid_login_generates_token(self):
        """Tests token is generated on successful login."""
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(self.logins),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("token", response_msg)

    def test_invalid_username_login(self):
        """Tests unauthorized error raised with invalid username."""
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="invalid",
                                                      password="testpass")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_invalid_password_login(self):
        """Tests unauthorized error raised with invalid password."""
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="testuser",
                                                      password="invalid")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("invalid", response_msg["Message"])

    def test_logout(self):
        """Test logout success"""
        response = self.app.delete(
            '/api/v1/auth/logout',
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 202)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("out", response_msg["Message"])

    """At this stage previous test data needs to be cleared"""

    def tearDown(self):
        """ clear data after every test"""
        user_object.users.clear()

    def test_reset_password(self):
        """Register a user"""
        self.app.post('/api/v1/auth/register', data=json.dumps(self.user),
                      headers={"content-type": "application/json"})

        """login the just registered user and get a token"""
        self.login = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(
                self.logins),
            content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']
        """Then reset their password with the new token"""
        response = self.app.put(
            '/api/v1/auth/reset-password',
            data=json.dumps(
                dict(
                    password="new_pass")),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 202)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("updated", response_msg["Message"])

    def test_get_all_users(self):
        """Test if get method gets all registered users"""
        response = self.app.get('/api/v1/auth/users',
                                content_type="application/json",
                                headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
