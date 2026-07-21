import unittest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.app import create_app

class TestAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app, cls.socketio = create_app()
        cls.client = cls.app.test_client()
        # Disable rate limiting for tests if possible, or use a test config
        cls.app.config['TESTING'] = True

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        
    def test_new_session(self):
        response = self.client.get('/api/session/new')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('session_id', data)
        
    def test_detect_language_api(self):
        # English
        response = self.client.post('/api/language/detect', 
                                  json={"text": "Hello world"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['detected_language'], 'en')
        
        # Hindi
        response = self.client.post('/api/language/detect', 
                                  json={"text": "नमस्ते"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['detected_language'], 'hi')

if __name__ == '__main__':
    unittest.main()
