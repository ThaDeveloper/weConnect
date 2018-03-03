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

class TestBusinessClassFunctionality(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.business_id = 1

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
        resp = self.app.get('api/businesses/222')
        self.assertEqual(resp.status_code, 404)
    
#makes tests executable
if __name__ == "__main__":
    unittest.main()