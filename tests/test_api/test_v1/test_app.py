"""Unit test for the Flask application."""
import unittest
from api.v1.app import app
import json


class TestApp(unittest.TestCase):
    """Test the Flask application."""

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_app_route_api_v1_status(self):
        """Route "/api/v1/status" should return "{"status": "OK"}"."""
        response = self.app.get('/api/v1/status')

        # Convert the response to JSON
        response_json = json.loads(response.data.decode())

        expected = {"status": "OK"}
        self.assertTrue(response_json, expected)
