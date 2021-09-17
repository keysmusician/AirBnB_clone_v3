#!/usr/bin/python3
"""Creates a route that returns a JSON"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status_check():
    """Returns JSON with 'OK' status check"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats')
def class_total():
    """Retrieves the number of each object by type"""
    stats = {}
    class_list = [Amenity, City, Place, Review, State, User]
    for class_type in class_list:
        stats[type(class_type).__name__] = storage.count(class_type)
    return jsonify(stats)
