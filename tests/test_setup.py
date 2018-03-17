import json
import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from src import app


class TestSetUp(unittest.TestCase):
    """Initialize the app with test data"""

    def setUp(self):
        self.app = app.test_client()
        self.user = {"username": "testuser", "password": "testpass"}
        self.unknownuser = {"username": "unkownuser", "password": "password"}
        self.business = {"name": "Google",
                         "description": "Its awesome",
                         "location": "CA",
                         "category": "Technology"}
        self.empty_business = {"name": "", "description": "", "location": "",
                               "category": ""}
        self.new_business = {"name": "Apple",
                             "description": "", "location": "",
                             "category": ""}
        self.register = self.app.post('/api/v1/auth/register',
                                      data=json.dumps(self.user),
                                      headers={"content-type":
                                               "application/json"})
        self.login = self.app.post('/api/v1/auth/login',
                                   data=json.dumps(self.user),
                                   content_type='application/json')
        
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']
        self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(
                self.unknownuser),
            content_type="application/json")
        self.unkownlogin = self.app.post("/api/v1/auth/login",
                                         data=json.dumps(self.unknownuser),
                                         content_type="application/json")
        self.data = json.loads(self.unkownlogin.get_data(as_text=True))
        self.unkowntoken = self.data['token']
