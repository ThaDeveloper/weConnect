import unittest
import json
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from tests.v2.test_setup import TestSetUp
from src.v2.models import User


class UserAuthClass(TestSetUp):
    """
    Test user authorization.
    """

    def test_user_can_register(self):
        """Test new user can be added to the system."""
        response = self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                dict(
                    username="testusername",
                    password="testpassword",
                    first_name="test",
                    last_name="username")),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("registered", response_msg["Message"])

    def test_blank_username(self):
        """Tests error raised with username missing."""
        response = self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                dict(
                    username="",
                    password="testpass",
                    first_name="blank",
                    last_name="username")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_username_has_space(self):
        """Tests error raised when username contains spaces."""
        response = self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                dict(
                    username="first last",
                    password="testpass",
                    first_name="first",
                    last_name="last")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("spaces", response_msg["Message"])

    def test_username_has_enough_characters(self):
        """Tests error raised when username has less then 3 characters."""
        response = self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                dict(
                    username="am",
                    password="testpass",
                    first_name="first",
                    last_name="last")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("characters", response_msg["Message"])

    def test_missing_password(self):
        """Tests error raised when password is missing."""
        response = self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                dict(
                    username="testusername",
                    password="",
                    first_name="first",
                    last_name="last")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_missing_first_or_last_name(self):
        """Tests error raised when first name or last name is missing."""
        response = self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                dict(
                    username="testusername",
                    password="testpassword",
                    first_name="",
                    last_name="last")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_username_isstring(self):
        """Tests error raised when wrong username format is provided."""
        response = self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                dict(
                    username=1234,
                    password="testpass",
                    first_name="first",
                    last_name="last")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Wrong", response_msg["Message"])

    def test_duplicate_users(self):
        """
        Tests for duplicate usernames
        """
        response = self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                dict(
                    username="testuser",
                    password="password",
                    first_name="first",
                    last_name="last")),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])

    def test_valid_login_generates_token(self):
        """Tests token is generated on successful login."""
        response = self.app.post("/api/v2/auth/login",
                                 data=json.dumps(self.user),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("token", response_msg)

    def test_missing_credentials(self):
        """Tests error raised for missing auth details."""
        response = self.app.post(
            "/api/v2/auth/login",
            data=json.dumps(
                dict(
                    username="",
                    password="")),
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_invalid_username_login(self):
        """Tests unauthorized error raised with invalid username."""
        response = self.app.post("/api/v2/auth/login",
                                 data=json.dumps(dict(username="invalid",
                                                      password="testpass")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_invalid_password_login(self):
        """Tests unauthorized error raised with invalid password."""
        response = self.app.post("/api/v2/auth/login",
                                 data=json.dumps(dict(username="testuser",
                                                      password="invalid")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("invalid", response_msg["Message"])

    def test_logout(self):
        """Test logout success"""
        response = self.app.delete(
            '/api/v2/auth/logout',
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("out", response_msg["Message"])

    def test_double_logout(self):
        """Test Re-logout"""
        self.app.delete(
            '/api/v2/auth/logout',
            headers={
                "x-access-token": self.token})
        response = self.app.delete(
            '/api/v2/auth/logout',
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Already", response_msg["Message"])

    def test_reset_password(self):
        """Register a user"""
        self.app.post(
            '/api/v2/auth/register',
            data=json.dumps(
                dict(
                    username="testreset",
                    password="pass", first_name="first", last_name="last")),
            headers={
                "content-type": "application/json"})

        # login the just registered user and get a token
        self.login = self.app.post(
            '/api/v2/auth/login',
            data=json.dumps(dict(username="testreset",
                                 password="pass")),
            content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']
        # Then reset their password with the new token
        response = self.app.put(
            '/api/v2/auth/reset-password',
            data=json.dumps(
                dict(username="testreset",
                     password="new_pass")),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 202)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("updated", response_msg["Message"])

    def test_get_one_user(self):
        """Tests authorized user can get a specific user profile"""
        response = self.app.get(
            '/api/v2/auth/users/{}'.format(
                User.query.order_by(
                    User.created_at).first().id),
            content_type="application/json",
            headers={
                "x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 200)

    def test_get_all_users(self):
        """Test if get method gets all registered users"""
        response = self.app.get('/api/v2/auth/users',
                                content_type="application/json",
                                headers={"x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 200)

    def test_get_all_users_unauthorized(self):
        """Tests error raised for accessing user list for non-admins"""
        response = self.app.get('/api/v2/auth/users',
                                content_type="application/json",
                                headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Cannot perform", response_msg["Message"])

    def test_get_one_user_unauthorized(self):
        """Tests error raised for accessing a user for non-admin"""
        response = self.app.get(
            '/api/v2/auth/users/{}'.format(
                User.query.order_by(
                    User.created_at).first().id),
            content_type="application/json",
            headers={
                "x-access-token": self.unkowntoken})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Cannot perform", response_msg["Message"])

    def test_get_user_404(self):
        """Test error raised when accessing nonexisting user"""
        response = self.app.get('/api/v2/auth/users/00',
                                content_type="application/json",
                                headers={"x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_promote_user(self):
        """Test error raised when accessing nonexisting user"""
        response = self.app.put(
            '/api/v2/auth/users/{}'.format(
                User.query.order_by(
                    User.created_at).first().id),
            content_type="application/json",
            headers={
                "x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("admin", response_msg["Message"])

    def test_unauthorized_promote_user(self):
        """Test error raised for unauthorized user promotion"""
        response = self.app.put(
            '/api/v2/auth/users/{}'.format(
                User.query.order_by(
                    User.created_at).first().id),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Cannot perform", response_msg["Message"])

    def test_delete_user(self):
        """Tests deleting user from db"""
        response = self.app.delete(
            '/api/v2/auth/users/{}'.format(
                User.query.order_by(
                    User.created_at).first().id),
            content_type="application/json",
            headers={
                "x-access-token": self.admintoken})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("deleted", response_msg["Message"])

    def test_unauthorized_user_delete(self):
        """Tests error raised for unauthorized user delete from db"""
        response = self.app.delete(
            '/api/v2/auth/users/{}'.format(
                User.query.order_by(
                    User.created_at).first().id),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Cannot perform", response_msg["Message"])

    def test_read_user_businesses(self):
        """Tests user can read the businesses of a particular user"""
        response = self.app.get(
            '/api/v2/auth/users/{}/businesses'.format(
                User.query.order_by(
                    User.created_at).first().id),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
