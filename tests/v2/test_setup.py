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
from src.v2.models import User, Business, Review
from config import Testing


class TestSetUp(unittest.TestCase):
    """Initialize the app with test data"""

    def setUp(self):
        app.config.from_object('config.Testing')
        self.app = app.test_client()
        db.create_all()
        self.user = {"username": "testuser", "password": "testpass", "first_name": "Test", "last_name": "User"}
        self.unknownuser = {"username": "unkownuser", "password": "password", "first_name":"Unkown", "last_name": "User"}
        self.admin = {
            "username": "testadmin",
            "password": "password",
            "first_name": "Test",
            "last_name": "admin",
            "admin": True}
        self.business = {"name": "Google",
                         "description": "Its awesome",
                         "location": "CA",
                         "category": "Technology"}
        self.empty_business = {"name": "", "description": "", "location": "",
                               "category": ""}
        self.new_business = {"name": "Apple",
                             "description": "", "location": "",
                             "category": ""}
        # Register and login a testuser
        self.register = self.app.post('/api/v2/auth/register',
                                      data=json.dumps(self.user),
                                      headers={"content-type":
                                               "application/json"})
        self.login = self.app.post('/api/v2/auth/login',
                                   data=json.dumps(self.user),
                                   content_type='application/json')

        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']
        # Register and login a testunkownuser
        self.app.post(
            "/api/v2/auth/register",
            data=json.dumps(
                self.unknownuser),
            content_type="application/json")
        self.unkownlogin = self.app.post("/api/v2/auth/login",
                                         data=json.dumps(self.unknownuser),
                                         content_type="application/json")
        self.data = json.loads(self.unkownlogin.get_data(as_text=True))
        self.unkowntoken = self.data['token']

        # register and login test admin
        self.app.post('/api/v2/auth/register',
                      data=json.dumps(self.admin),
                      headers={"content-type":
                               "application/json"})
        self.adminlogin = self.app.post('/api/v2/auth/login',
                                        data=json.dumps(self.admin),
                                        content_type='application/json')

        self.data = json.loads(self.adminlogin.get_data(as_text=True))
        self.admintoken = self.data['token']

        self.app.post('/api/v2/businesses', data=json.dumps(dict(name="testclient", description="This is just for setup", location="testing", category="unittest")),
                      content_type="application/json",
                      headers={"x-access-token": self.token})
        business = {
            "name": "Andela Kenya",
            "description": "Become world class",
            "location": "Nairobi",
            "category": "Tech"}
        test_business = Business()
        test_business.import_data(business)
        test_business.user_id = User.query.order_by(User.created_at).first().id

        business2 = {
            "name": "M-Kopa",
            "description": "Mwangaza mashinani",
            "location": "Nairobi",
            "category": "Tech"}
        test_business2 = Business()
        test_business2.import_data(business2)
        test_business2.user_id = User.query.order_by(
            User.created_at).first().id

        business3 = {
            "name": "Google Kenya",
            "description": "Skynet here I come",
            "location": "Nairobi",
            "category": "Tech"}
        test_business3 = Business()
        test_business3.import_data(business3)
        test_business3.user_id = User.query.order_by(
            User.created_at).first().id

        review = {"title": "Great culture",
                  "message": "Its a great place to grow"}
        test_review = Review()
        test_review.import_data(review)
        test_review.business_id = Business.query.order_by(Business.created_at).first().id
        test_review.user_id = User.query.order_by(User.created_at).first().id

        db.session.add(test_business)
        db.session.add(test_business2)
        db.session.add(test_business3)
        db.session.add(test_review)
        db.session.commit()

    def tearDown(self):
        """Drops the db."""
        # db.session.remove()
        # db.drop_all()
        db.session.query(Review).delete()
        db.session.commit()
        db.session.query(Business).delete()
        db.session.commit()
        db.session.query(User).delete()
        db.session.commit()
