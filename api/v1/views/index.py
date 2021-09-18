#!/usr/bin/python3
"""Creates a route that returns a JSON"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status_check():
    """Returns JSON with 'OK' status check"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def class_total():
    """Retrieves the number of each object by type"""
    class_counts = {
        "amenities": storage.count("Amenities"),
        "cities": storage.count("Cities"),
        "places": storage.count("Places"),
        "reviews": storage.count("Reviews"),
        "states": storage.count("States"),
        "users": storage.count("Users")
    }

    return jsonify(class_counts)
