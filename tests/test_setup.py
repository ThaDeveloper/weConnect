import json
import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from src import app, db
from src.models import User, Business, Review
from config import Testing


class TestSetUp(unittest.TestCase):
    """Initialize the app with test data"""

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
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

        business = {
            "name": "Andela",
            "description": "Become worldclass",
            "location": "Nairobi",
            "category": "Tech"}
        test_business = Business()
        test_business.import_data(business)
        test_business.user_id = 1

        business2 = {
            "name": "M-Kopa",
            "description": "Mwangaza mashinani",
            "location": "Nairobi",
            "category": "Tech"}
        test_business2 = Business()
        test_business2.import_data(business2)
        test_business2.user_id = 1

        business3 = {
            "name": "Google Kenya",
            "description": "Skynet here I come",
            "location": "Nairobi",
            "category": "Tech"}
        test_business3 = Business()
        test_business3.import_data(business3)
        test_business3.user_id = 2

        review = {"title": "Great culture",
                  "message": "Its a great place to grow"}
        test_review = Review()
        test_review.import_data(review)
        test_review.business_id = 1
        test_review.user_id = 1

        db.session.add(test_business)
        db.session.add(test_business2)
        db.session.add(test_business3)
        db.session.add(review)
        db.session.commit()

    def tearDown(self):
        """Drops the db."""
        db.session.remove()
        db.drop_all()
