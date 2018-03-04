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

class TestBusinessClassFunctionality(TestSetUp):
    
    def test_business_access_with_invalid_token(self):
        """Raise unauthorized error invalid token."""
        response = self.app.post("/api/businesses/",
                                    data=json.dumps(dict(name="business")),
                                    content_type="application/json",
                                    headers={"Authorization": "Token " + "invalid"})
        self.assertEqual(response.status_code, 401)

    def test_add_new_business(self):
        """Tests creating a new business."""
        response = self.app.post("/api/businesses/",
                                    data=json.dumps(dict(name="business")),
                                    content_type="application/json",
                                    headers={"Authorization": "Token " + self.token})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data)
        self.assertIn("Business", response_msg["Message"])

    def test_invalid_name(self):
        """Error raised for blank business name. A business must have  a name."""
        response = self.app.post("/api/businesses/",
                                    data=json.dumps(dict(name="")),
                                    content_type="application/json",
                                    headers={"Authorization": "Token " + self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data)
        self.assertIn("A business must have a name", response_msg["Message"])

    def test_duplicates_prevented(self):
        """
        Error raised for duplicate business names.
        """
        response = self.app.post("/api/businesses/",
                                    data=json.dumps(dict(name="business_name")),
                                    content_type="application/json",
                                    headers={"Authorization": "Token " + self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data)
        self.assertIn("already exists", response_msg["Message"])

    def test_business_list(self):
        resp = self.app.get('/api/businesses')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0], {
            'id': 1,
            'name': 'Ventures',
            'description': 'Great Business',
            'location': 'nairobi',
            'category': 'realestate',
            'user_id': 1
        })
    def test_business_detail_200(self):
        resp = self.app.get('/api/businesses/{}'.format(self.business_id))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(content, {
            'id': 1,
            'name': 'Ventures',
            'description': 'Great Business',
            'location': 'nairobi',
            'category': 'realestate',
            'user_id': 1
        })
    
    def test_business_detail_404(self):
        resp = self.app.get('/api/businesses/222')
        self.assertEqual(resp.status_code, 404)
    

    def test_invalid_business_request(self):
        """
        Error raised for invalid business request.
        """
        response = self.app.get("/api/businesses/3",
                                   content_type="application/json",
                                   headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data)
        self.assertIn("not found", response_msg["Message"])

    def test_update_business(self):
        """Tests a business can be updated."""
        response = self.app.put("/api/businesses/2",
                                   data=json.dumps(dict(name="updated_name")),
                                   content_type="application/json",
                                   headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data)
        self.assertIn("New_Name", response_msg["Message"])

    def test_invalid_update(self):
        """Error raised for invalid update request."""
        response = self.app.put("/api/businnesses/3",
                                   data=json.dumps(dict(name="updated_name")),
                                   content_type="application/json",
                                   headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data)
        self.assertIn("not found", response_msg["Message"])    

    def test_delete_business(self):
        """Tests business deletion."""
        response = self.app.delete("/api/businesses/1",
                                      content_type="application/json",
                                      headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data)
        self.assertIn("deleted", response_msg["Message"])

    def test_invalid_delete(self):
        """Error raised for invalid delete request."""
        response = self.app.delete("/api/businesses/3",
                                      content_type="application/json",
                                      headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data)
        self.assertIn("not found", response_msg["Message"])

    def test_duplicate_updates(self):
        """
        Tests for updating business to a name that already exists.
         """
        response = self.app.put("/api/businesses/1",
                                   data=json.dumps(dict(name="testbusiness")),
                                   content_type="application/json",
                                   headers={"Authorization": "Token " + self.token})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data)
        self.assertIn("already exists", response_msg["Message"])

    def test_search_by_business_name(self):
        """Tests user can search for business."""
        response = self.app.get("/api/businesses/?q=testbusiness",
                                   content_type="application/json",
                                   headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data)
        self.assertEqual("testbusiness", response_msg["Businesses"][0]["name"])

    def test_invalid_search(self):
        """ Tests for invalid business search."""
        response = self.app.get("/api/businesses/?q=invalid",
                                   content_type="application/json",
                                   headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data)
        self.assertIn("not found", response_msg["Message"])

#makes tests executable
if __name__ == "__main__":
    unittest.main()
