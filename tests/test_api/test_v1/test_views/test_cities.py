#!/usr/bin/python3
"""Unit test for the API cities view"""
from api.v1.app import app
from models.city import City
from models.state import State
import MySQLdb
from test_env import test_environment_is_set
import unittest


@unittest.skipUnless(test_environment_is_set(), "Test environment is not set")
class TestAppAPIv1Cities(unittest.TestCase):
    """Tests the Flask application /api/v1/states routes"""

    def setUp(self):
        """Set up testing environment."""
        app.testing = True
        self.test_client = app.test_client()
        self.test_client.testing = True

        # Connect to the the test database
        self.db = MySQLdb.connect(
            user='hbnb_test', passwd='hbnb_test_pwd', db='hbnb_test_db'
        )

    def tearDown(self):
        """Teardown"""
        self.db.close()

    def test_states_ID_cities_GET(self):
        """
        Requesting this route should return a list of all cities linked to a
        state
        """
        state = State(name='Testachusetts')
        state.save()
        id = state.id

        testville = City(name='Testville', state_id=id)
        testville.save()

        testington = City(name='Testington', state_id=id)
        testington.save()

        # Request the resource
        response = self.test_client.get('/api/v1/states/{}/cities/'.format(id))

        # Deserialize the response
        data = response.json

        # Validate content
        self.assertIsInstance(data, list)
        for element in data:
            self.assertIsInstance(element, dict)

        cities = [testville.to_dict(), testington.to_dict()]
        self.assertCountEqual(data, cities)

    def test_states_INVALID_ID_cities_GET(self):
        """Requesting this route with an invalid should return 404"""
        response = self.test_client.get('/api/v1/states/INVALID_ID/cities/')
        self.assertEqual(response.status_code, 404)

        data = response.json
        error_json = {'error': 'Not found'}
        self.assertEqual(data, error_json)

    def test_cities_ID_GET(self):
        """
        Requesting this route should return the JSON for the city with the
        specified ID
        """
        pass
