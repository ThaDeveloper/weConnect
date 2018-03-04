import os
import json
import unittest
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# from src.api import app
from tests.test_setup import TestSetUp

class TestReviewsClassFunctionality(TestSetUp):

    def test_add_new_review(self):
        """Tests a new review can be added."""
        response = self.app.post("/api/businesses/1/reviews",
                                    data=json.dumps(dict(title="testbusinessreview",
                                                         message="I love working here")),
                                    content_type="application/json",
                                    headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data)
        self.assertIn("Testbusinessreview", response_msg["Message"])

    def test_missing_title(self):
        """Tests error raised for misisng review title."""
        response = self.app.post("/api/businesses/1/reviews",
                                    data=json.dumps(dict(title="",
                                                         message="Low pay")),
                                    content_type="application/json",
                                    headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data)
        self.assertIn("must have a title", response_msg["Message"])
    
    def test_get_all_reviewss(self):
        """Tests listing all reviews."""
        response = self.app.get("/api/businesses/reviews",
                                   content_type="application/json",
                                   headers={'Authorization': 'Token ' + self.token})
        response_msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_msg["Reviews"]), 2)

    def test_delete_review(self):
        """Tests a review can be deleted."""
        response = self.app.delete("/api/businesses/1/reviews/1",
                                      content_type="application/json",
                                      headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data)
        self.assertIn("deleted", response_msg["Message"])

    def test_invalid_delete(self):
        """Tests error raised for an invalid delete request."""
        response = self.app.delete("/api/businesses/1/reviews/2",
                                      content_type="application/json",
                                      headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data)
        self.assertIn("not found", response_msg["Message"])



