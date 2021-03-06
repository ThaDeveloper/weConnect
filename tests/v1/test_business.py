import json
import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from tests.v1.test_setup import TestSetUp


class TestBusinessClassFunctionality(TestSetUp):
    def test_business_access_with_invalid_token(self):
        """Raise unauthorized error invalid token."""
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(self.business),
                                 content_type="application/json",
                                 headers={"x-access-token": "Wrong token"})
        self.assertEqual(response.status_code, 401)

    def test_add_new_business(self):
        """Tests creating a new business."""
        response = self.app.post('/api/v1/businesses',
                                 data=json.dumps(self.business),
                                 content_type="application/json",
                                 headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business", response_msg["Message"])

    def test_empty_name(self):
        """Error raised for blank business name.
        A business must have  a name."""
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(dict(name="")),
                                 content_type="application/json",
                                 headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("required", response_msg["Message"])

    def test_duplicates_prevented(self):
        """
        Error raised for duplicate business names.
        """
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(dict(name="Google",
                                                      description="",
                                                      location="",
                                                      category="")),
                                 content_type="application/json",
                                 headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])

    def test_business_list(self):
        resp = self.app.get('/api/v1/businesses')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_business_detail_200(self):
        """Test if you can get a single business.
        Register a single business first"""
        self.app.post('/api/v1/businesses', data=json.dumps(self.business),
                      content_type="application/json",
                      headers={"x-access-token": self.token})
        resp = self.app.get('/api/v1/businesses/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_invalid_business_request(self):
        """
        Error raised for invalid business request.
        """
        resp = self.app.get("/api/v1/businesses/15")
        self.assertEqual(resp.status_code, 404)
        response_msg = json.loads(resp.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_update_business(self):
        """Tests a business can be updated."""
        response = self.app.put("/api/v1/businesses/1",
                                data=json.dumps(self.new_business),
                                content_type="application/json",
                                headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("updated", response_msg["Message"])

    def test_invalid_update(self):
        """Error raised for invalid update request."""
        response = self.app.put("/api/v1/businesses/3",
                                data=json.dumps(self.new_business),
                                content_type="application/json",
                                headers={"x-access-token": self.token})

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_updating_unauthorized_business(self):
        """Tests error raised when updating someone else's business."""
        response = self.app.put("/api/v1/businesses/1",
                                data=json.dumps(self.new_business),
                                content_type="application/json",
                                headers={"x-access-token": self.unkowntoken})

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Unauthorized", response_msg["Message"])

    def test_duplicate_updates(self):
        """
        Tests for updating business to a name that already exists.
         """
        response = self.app.put("/api/v1/businesses/1",
                                data=json.dumps(self.business),
                                content_type="application/json",
                                headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already exists", response_msg["Message"])

    def test_delete_business(self):
        """Tests business deletion."""
        self.app.post(
            '/api/v1/businesses',
            data=json.dumps(
                dict(
                    name="Andela",
                    description="",
                    location="",
                    category="")),
            content_type="application/json",
            headers={
                "x-access-token": self.token})
        response = self.app.delete("/api/v1/businesses/2",
                                   content_type="application/json",
                                   headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("deleted", response_msg["Message"])

    def test_deleting_unauthorized_business(self):
        """Tests error raised when deleting someone else's business."""
        response = self.app.delete(
            "/api/v1/businesses/1",
            data=json.dumps(
                self.new_business),
            content_type="application/json",
            headers={
                "x-access-token": self.unkowntoken})

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Unauthorized", response_msg["Message"])

    def test_invalid_delete(self):
        """Error raised for invalid delete request."""
        response = self.app.delete("/api/v1/businesses/10",
                                   content_type="application/json",
                                   headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("not found", response_msg["Message"])

    def test_unauthorized_delete(self):
        response = self.app.delete("/api/v1/businesses/2",
                                   content_type="application/json",
                                   headers={"x-access-token": "dd"})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Invalid", response_msg["Message"])


if __name__ == "__main__":
    unittest.main()
