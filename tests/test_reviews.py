import os
import json
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from tests.setup import TestSetUp


class TestReviewsClassFunctionality(TestSetUp):

    def test_add_new_review(self):
        """Tests a new review can be added."""
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


"""These tests will be for future version of the api"""
#     def test_delete_review(self):
#         """Tests a review can be deleted."""
#         response = self.app.delete("/api/businesses/1/reviews/1",
#                                       content_type="application/json",
#                                       headers={'Authorization': 'Token '
#                                        + self.token})
#         self.assertEqual(response.status_code, 200)
#         response_msg = json.loads(response.data)
#         self.assertIn("deleted", response_msg["Message"])

#     def test_invalid_delete(self):
#         """Tests error raised for an invalid delete request."""
#         response = self.app.delete("/api/businesses/1/reviews/2",
#                                       content_type="application/json",
#                                       headers={'Authorization': 'Token '
#                                        + self.token})
#         self.assertEqual(response.status_code, 404)
#         response_msg = json.loads(response.data)
#         self.assertIn("not found", response_msg["Message"])
