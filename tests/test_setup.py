import os
import json
import unittest
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.api import app


class TestSetUp(unittest.TestCase):
    """Initialize the app with test data"""
    def setUp(self):
        self.app = app.test_client()
        self.business_id = 1
        self.app.post("/api/auth/register",
                         data=json.dumps(dict(username="username",
                                              password="pass")),
                         content_type="application/json")

        response = self.app.post("/api/auth/login",
                                    data=json.dumps(dict(username="username",
                                                    password="pass")),
                                    content_type="application/json")
        response_msg = json.loads(response.data)
        self.token = response_msg["Token"]