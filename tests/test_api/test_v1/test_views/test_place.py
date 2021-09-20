#!/usr/bin/python3
"""Unit test for the API places view"""
from api.v1.app import app
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
import MySQLdb
import unittest


class TestAppAPIv1Places(unittest.TestCase):
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

    def test_app_route_api_v1_cities_cityID_places_GET(self):
        """
        Api route 'cities/<city_id>/places' should return a list of all Places
        """
        state = State(name='New State')
        state.save()
        city = City(name='New Citysburg', state_id=state.id)
        city.save()
        user = User(name='John Doe', email='NULL', password='NULL')
        user.save()
        place = Place(name='Fancy place', city_id=city.id, user_id=user.id)
        place.save()

        # Request the resource
        response = self.test_client.get(
            '/api/v1/cities/{}/places'.format(city.id)
        )

        # Deserialize the response
        response_json = response.json

        # Confirm response content
        expected = [place.to_dict()]
        self.assertEqual(response_json, expected)
