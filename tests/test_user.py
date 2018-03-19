import unittest
import json
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
    Test user authorization.
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

    def test_username_has_space(self):
        """Tests error raised when username contains spaces."""
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(username="firt last",
                                                      password="testpass")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("spaces", response_msg["Message"])

    def test_username_has_enouh_characters(self):
        """Tests error raised when username has less then 3 characters."""
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(username="am",
                                                      password="testpass")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("characters", response_msg["Message"])

    def test_missing_password(self):
        """Tests error raised when password is missing."""
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(username="testusername",
                                                      password="")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_username_isstring(self):
        """Tests error raised when wrong username format is provided."""
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(username=1234,
                                                      password="testpass")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Wrong", response_msg["Message"])

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
                                 data=json.dumps(self.user),
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
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("out", response_msg["Message"])

    def test_double_logout(self):
        """Test Re-logout"""
        self.app.delete(
            '/api/v1/auth/logout',
            headers={
                "x-access-token": self.token})
        response = self.app.delete(
            '/api/v1/auth/logout',
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Already", response_msg["Message"])

    def test_reset_password(self):
        """Register a user"""
        self.app.post('/api/v1/auth/register', data=json.dumps(self.user),
                      headers={"content-type": "application/json"})

        # login the just registered user and get a token
        self.login = self.app.post(
            '/api/v1/auth/login',
            data=json.dumps(
                self.user),
            content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']
        # Then reset their password with the new token
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

    def test_get_user_404(self):
        """Test error raised when accessing nonexisting user"""
        response = self.app.get('/api/v1/auth/users/10',
                                content_type="application/json")
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])
    
    def test_promote_user(self):
        """Test error raised when accessing nonexisting user"""
        response = self.app.put('/api/v1/auth/users/1',
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("admin", response_msg["Message"])

    def test_delete_user(self):
        """Tests deleting user from db"""
        response = self.app.delete('/api/v1/auth/users/1',
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("deleted", response_msg["Message"])

if __name__ == '__main__':
    unittest.main()
