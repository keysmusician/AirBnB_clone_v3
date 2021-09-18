#!/usr/bin/python3
"""Creates index routes"""
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


@app_views.route('/stats')
def class_total():
    """Retrieves the number of each object by type"""
    class_counts = {
        "amenities": storage.count(Amenity),
        "cities":    storage.count(City),
        "places":    storage.count(Place),
        "reviews":   storage.count(Review),
        "states":    storage.count(State),
        "users":     storage.count(User)
    }

    return jsonify(class_counts)
