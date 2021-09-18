#!/usr/bin/python3
"""Unit test for the Flask application"""
from api.v1.app import app
import json
import MySQLdb
import unittest


class TestAppIndex(unittest.TestCase):
    """Tests the Flask application API routes"""

    def setUp(self):
        """Set up testing environment."""
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Set up the test database
        self.db = MySQLdb.connect(
            user='hbnb_test', passwd='hbnb_test_pwd', db='hbnb_test_db'
        )

    def tearDown(self):
        self.db.close()

    def test_app_route_api_v1_status(self):
        """Route '/api/v1/status' should return {"status": "OK"}."""
        # Request the resource
        response = self.app.get('/api/v1/status')

        # Deserialize the response
        response_json = json.loads(response.data.decode())

        expected = {"status": "OK"}
        self.assertEqual(response_json, expected)

    #! Response values need to be checked!
    def test_app_route_api_v1_stats(self):
        """
        Route '/api/v1/stats' should return a count of each model in storage.
        """
        # Request the resource
        response = self.app.get('/api/v1/stats')

        # Deserialize the response
        response_json = json.loads(response.data.decode())

        # All of and only these keys should exist in the response
        expected_keys = [
            "amenities",
            "cities",
            "places",
            "reviews",
            "states",
            "users"
        ]
        response_keys = list(response_json.keys())
        expected_keys.sort()
        response_keys.sort()

        # Check the keys
        self.assertListEqual(response_keys, expected_keys)

        """
        query_str = \"""
        SELECT * from states,
        \"""
        cursor = self.db.cursor()
        cursor.execute(query_str)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        """

if __name__ == '__main__':
    unittest.main()
