#!/usr/bin/python3
"""Unit test for the States view"""
import re
from models.state import State
from api.v1.app import app
import json
import MySQLdb
from os import environ
import unittest


test_environment = {
    'HBNB_MYSQL_USER': 'hbnb_test',
    'HBNB_MYSQL_PWD': 'hbnb_test_pwd',
    'HBNB_MYSQL_HOST': 'localhost',
    'HBNB_MYSQL_DB': 'hbnb_test_db',
    'HBNB_TYPE_STORAGE': 'db'
}

# Ensure tests were executed in the test environment
# ? This mainly ensures the test database is used.
for key, value in test_environment.items():
    if environ.get(key) != value:
        raise EnvironmentError(
            'Do not run this test outside of the test environment.'
        )

class TestAppIndex(unittest.TestCase):
    """Tests the Flask application API routes"""

    def setUp(self):
        """Set up testing environment."""
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Connect to the the test database
        self.db = MySQLdb.connect(
            user='hbnb_test', passwd='hbnb_test_pwd', db='hbnb_test_db'
        )

    def tearDown(self):
        self.db.close()

    #! Response content needs testing
    def test_app_GET_route_api_v1_states(self):
        """
        Requesting this route should return a list of all state objects
        """
        # Request the resource
        response = self.app.get('/api/v1/states')

        # Deserialize the response
        response_data = json.loads(response.data.decode())

        self.assertIsInstance(response_data, list)

    def test_app_GET_route_api_v1_state_id(self):
        """
        Requesting this route should return the State object with the
        specified ID
        """
        # Create a new State and submit in into the database
        new_state = State(name='Testonia')
        id = new_state.id
        new_state.save()

        # Request the new State by id via the API
        response = self.app.get('/api/v1/states/{}'.format(id))

        # Deserialize the response
        response_id = json.loads(response.data.decode()).get('id')
        self.assertEqual(
            response_id, id, "API response returned wrong or missing ID"
        )

    def test_app_GET_route_api_v1_state_id_RAISES_404(self):
        """Requesting this route with an invalid ID should return 404"""
        response = self.app.get('/api/v1/states/404')

        self.assertEqual(
            response.status_code, 404, "API returned wrong status code."
        )

    def test_app_DELETE_route_api_v1_state_id(self):
        """
        Requesting this route should return the state object with the
        corresponding ID
        """

        # Create a new state
        testonia = State(name='Testonia')
        id = testonia.id

        # Enter it into the database
        # Note: State.save() is tested in TestState
        testonia.save()

        # Request to delete the resource
        response = self.app.delete('/api/v1/states/{}'.format(id))
        data = json.loads(response.data.decode())

        # Confirm the response content and status code
        self.assertEqual(data, {})
        self.assertEqual(response.status_code, 200)

        # Confirm the State is not in the databse
        db_cursor = self.db.cursor()
        db_cursor.execute(
            "SELECT id FROM states WHERE id='{}'".format(testonia.id)
        )
        record = db_cursor.fetchone()
        db_cursor.close()
        self.assertIsNone(record)




    #! Incomplete
    def test_app_POST_route_api_v1_state_id(self):
        """
        Requesting this route should create a new state object, enter it in the
        database, and return it in JSON format
        """

        # Define State parameters

        # Request the resource
        response = self.app.post('/api/v1/states')

        # Assert the entry is in the database

    #! Incomplete
    def test_app_PUT_route_api_v1_state_id(self):
        """
        Requesting this route should create a new state object, enter it in the
        database, and return it in JSON format
        """

        # Define State parameters

        # Request the resource
        response = self.app.post('/api/v1/states')

        # Assert the entry is in the database

if __name__ == '__main__':
    unittest.main()
