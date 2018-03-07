import os
import json
import unittest
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.views import app,user_object


class TestSetUp(unittest.TestCase):
    """Initialize the app with test data"""
    def setUp(self):
        self.app = app.test_client()
        # self.business_id = 1
       
        self.user = {"username": "testuser", "password": "testpass"}
        self.logins = {"username": "testuser", "password": "testpass"}
        self.business = {"name": "Google", "description": "Its awesome", "location": "CA",
                         "category": "Technology"}
        self.empty_business = {"name": "", "description": "", "location": "",
                              "category": ""}
       
        # Create_user
        self.app.post('/api/v1/auth/register', data=json.dumps(self.user),
                           headers={"content-type": "application/json"})


        self.login = self.app.post('/api/v1/auth/login', data=json.dumps(self.logins),
                                        content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        # get the token to be used by tests
        self.token = self.data['token']

       
    