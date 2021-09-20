#!/usr/bin/python3
"""Creates cities view routes"""
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<id>/cities',  methods=['GET', 'POST'], strict_slashes=False)
def get_cities_of_state_by_id(id):
    """Returns a JSON list of all cities of a state."""
    state = storage.get(State, id)

    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])
    elif request.method == 'POST':
        post = request.get_json(silent=True)
        if post is None:
            return ("Not a JSON", 400)
        if type(post) is not dict:
            return ("Missing name", 400)
        name = post.get('name')
        if name is None:
            return ('Missing name', 400)
        new_city = City(name=name, state_id=state.id)
        new_city.save()
        return (jsonify(new_city.to_dict()), 201)


@app_views.route(
    '/cities/<id>',  methods=['DELETE', 'GET', 'PUT'], strict_slashes=False)
def get_city_by_id(id):
    """Returns JSON serialization of a city"""
    city = storage.get(City, id)

    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        city.delete()
        return ('{}', 200)
    elif request.method == 'PUT':
        # Get the update values
        post = request.get_json(silent=True)
        if post is None:
            return ('Not a JSON', 400)

        # Update the City
        for key, value in post.items():
            # Ignore these reserved keys
            if key in ('id', 'created_at', 'updated_at', 'state_id'):
                continue
            setattr(city, key, value)
        city.save()

        return (jsonify(city.to_dict()), 200)
