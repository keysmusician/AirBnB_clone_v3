#!/usr/bin/python3
"""Creates a route that returns a JSON"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status_check():
    """Returns JSON with 'OK' status check"""
    return jsonify({"status": "OK"})
