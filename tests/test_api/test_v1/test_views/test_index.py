#!/usr/bin/python3
"""Unit test for the API index view"""
from api.v1.app import app
import MySQLdb
import unittest


class TestAppAPIv1Index(unittest.TestCase):
    """Tests the Flask application API routes"""

    def setUp(self):
        """Set up testing environment"""
        app.testing = True
        self.test_client = app.test_client()

        # Set up the test database
        self.db = MySQLdb.connect(
            user='hbnb_test', passwd='hbnb_test_pwd', db='hbnb_test_db'
        )

    def tearDown(self):
        """Teardown routine"""
        self.db.close()

    def test_app_route_api_v1_status(self):
        """Route '/api/v1/status' should return {"status": "OK"}"""
        # Request the resource
        response = self.test_client.get('/api/v1/status')

        # Deserialize the response
        response_json = response.json

        expected = {"status": "OK"}
        self.assertEqual(response_json, expected)

    def test_app_route_api_v1_stats(self):
        """
        Route '/api/v1/stats' should return counts of each model in storage
        """
        # Request the resource
        response = self.test_client.get('/api/v1/stats')

        # Deserialize the response
        data = response.json

        # All of and only these keys should exist in the response
        expected_keys = [
            "amenities",
            "cities",
            "places",
            "reviews",
            "states",
            "users"
        ]
        response_keys = list(data.keys())

        # Check the keys
        self.assertCountEqual(response_keys, expected_keys)

        # Confirm the counts
        cursor = self.db.cursor()
        for table in expected_keys:
            cursor.execute("SELECT COUNT(*) from {}".format(table))
            result = cursor.fetchone()[0]
            self.assertEqual(data.get(table), result)
        cursor.close()

if __name__ == '__main__':
    unittest.main()
