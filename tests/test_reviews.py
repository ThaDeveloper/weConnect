import json
import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from tests.test_setup import TestSetUp


class TestReviewsClassFunctionality(TestSetUp):

    def test_add_new_review(self):
        """Tests a new review can be added."""
        self.app.post('/api/v1/businesses',
                      data=json.dumps(self.business),
                      content_type="application/json",
                      headers={"x-access-token": self.token})
        response = self.app.post(
            "/api/v1/businesses/1/reviews",
            data=json.dumps(
                dict(
                    title="testbusinessreview",
                    message="I love working here")),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("recorded", response_msg["Message"])

    def test_missing_title(self):
        """Tests error raised for misisng review title."""
        response = self.app.post("/api/v1/businesses/1/reviews",
                                 data=json.dumps(dict(title="",
                                                      message="Low pay")),
                                 content_type="application/json",
                                 headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_get_all_business_reviews(self):
        """Tests listing all reviews for a single business."""
        response = self.app.get("/api/v1/businesses/1/reviews",
                                content_type="application/json",
                                headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
