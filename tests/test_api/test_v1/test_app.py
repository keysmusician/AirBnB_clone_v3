#!/usr/bin/python3
"""Unit test for the Flask application"""
from api.v1.app import app
import json
# import MySQLdb
import unittest


class TestApp(unittest.TestCase):
    """Tests the Flask application API routes"""

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_app_route_api_v1_404(self):
        """
        Invalid '/api/v1/' endpoints should return {"error": "Not found"}
        """
        # Request an invalid resource
        response = self.app.get('/api/v1/404')

        # Deserialize the response
        response_json = json.loads(response.data.decode())

        expected = {"error": "Not found"}
        self.assertEqual(response_json, expected)
