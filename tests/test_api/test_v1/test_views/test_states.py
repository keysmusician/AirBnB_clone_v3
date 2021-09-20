#!/usr/bin/python3
"""Unit test for the API states view"""
from models.state import State
from api.v1.app import app
import json
import MySQLdb
from test_env import test_environment_is_set
import unittest


@unittest.skipUnless(test_environment_is_set(), "Test environment is not set")
class TestAppAPIv1States(unittest.TestCase):
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
        """Tear down"""
        self.db.close()

    def test_app_route_api_v1_states_GET(self):
        """
        Requesting this route should return a list of all State objects
        """
        # Request the resource
        response = self.test_client.get('/api/v1/states/')

        # Deserialize the response
        response_data = response.json

        # Compare count
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM states"
        )
        query_result = cursor.fetchone()
        cursor.close()

        api_count = len(response_data)
        mysqldb_count = query_result[0]

        self.assertEqual(api_count, mysqldb_count)

        # Validate content, if any
        if api_count > 0:
            expected_keys = \
                ['id', 'created_at', 'updated_at', 'name']
            response_keys = response_data[0].keys()
            self.assertTrue(
                all([key in response_keys for key in expected_keys])
            )

    def test_app_route_api_v1_states_id_GET(self):
        """
        Requesting this route should return the State object with the
        specified ID
        """
        # Create a new State and submit in into the database
        new_state = State(name='Testonia')
        id = new_state.id
        new_state.save()

        # Request the new State by id via the API
        response = self.test_client.get('/api/v1/states/{}'.format(id))

        # Deserialize the response
        response_id = response.json.get('id')
        self.assertEqual(
            response_id, id, "API response returned wrong or missing ID"
        )

    def test_app_route_api_v1_states_id_GET_RAISES_404(self):
        """Requesting this route with an invalid ID should return 404"""
        response = self.test_client.get('/api/v1/states/404')

        self.assertEqual(
            response.status_code, 404, "API returned wrong status code."
        )

    def test_app_route_api_v1_states_id_DELETE(self):
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
        response = self.test_client.delete('/api/v1/states/{}'.format(id))
        # ? Using response.json returns None if the JSON is empty,
        # ? so, explicitly parse the JSON instead:
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

    def test_app_route_api_v1_states_POST(self):
        """
        Requesting this route should create a new state object, enter it in the
        database, and return it in JSON format
        """

        # Define State parameters
        post_data = {'name': 'California'}

        # Request the resource
        response = self.test_client.post('/api/v1/states/', json=post_data)

        # Confirm server responded correctly
        self.assertEqual(response.status_code, 201)

        # Confirm response content
        response_data = response.json

        self.assertIsInstance(response_data, dict)
        self.assertEqual(response_data.get('__class__'), 'State')

        id = response_data.get('id')
        self.assertIsNotNone(id)

        # Confirm the entry is in the database
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT id FROM states WHERE id='{}'".format(id)
        )
        record = cursor.fetchone()
        cursor.close()

        self.assertIsNotNone(record)

    def test_app_route_api_v1_POST_bad_request(self):
        """
        Requesting this route without sending JSON containing 'name', or
        sending invalid JSON should return HTTP code 400.
        """
        response = self.test_client.post('/api/v1/states/', data='')
        self.assertEqual(response.status_code, 400)
        request_data = response.data.decode()
        self.assertEqual(request_data, 'Not a JSON')

        response = self.test_client.post('/api/v1/states/', json=[])
        self.assertEqual(response.status_code, 400)
        request_data = response.data.decode()
        self.assertEqual(request_data, 'Missing name')

        response = self.test_client.post('/api/v1/states/', json={})
        self.assertEqual(response.status_code, 400)
        request_data = response.data.decode()
        self.assertEqual(request_data, 'Missing name')

        response = self.test_client.post(
            '/api/v1/states/', json={'test': 'hello'}
        )
        self.assertEqual(response.status_code, 400)
        request_data = response.data.decode()
        self.assertEqual(request_data, 'Missing name')

    def test_app_route_api_v1_states_id_PUT(self):
        """
        Requesting this route should create a new state object, enter it in the
        database, and return it in JSON format
        """

        # Define State parameters to update
        post_data = {'name': 'New Testonia'}

        # Request the resource
        response = self.test_client.post('/api/v1/states/', json=post_data)
        id = response.json.get('id')
        self.assertIsNotNone(id)

        # Confirm the entry is in the database
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM states WHERE id='{}'".format(id))
        record = cursor.fetchone()
        cursor.close()

        self.assertIsNotNone(record)


if __name__ == '__main__':
    unittest.main()
