"""Unit test for the Flask application"""
import unittest
from api.v1.app import app
import json
# import MySQLdb


class TestAppIndex(unittest.TestCase):
    """Tests the Flask application routes"""

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_app_route_api_v1_status(self):
        """Route '/api/v1/status' should return {"status": "OK"}."""
        # Request the resource
        response = self.app.get('/api/v1/status')

        # Convert the response to JSON
        response_json = json.loads(response.data.decode())

        expected = {"status": "OK"}
        self.assertEqual(response_json, expected)

    #! Needs more accurate response check
    def test_app_route_api_v1_stats(self):
        """
        Route '/api/v1/stats' should return a count of each model in storage.
        """
        # Request the resource
        response = self.app.get('/api/v1/stats')

        # Convert the response to JSON
        response_json = json.loads(response.data.decode())

        # Check the result
        expected = None
        self.assertIsInstance(response_json, dict)
