#!/usr/bin/python3
"""Creates places view routes"""
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.place import Place



@app_views.route(
    '/cities/<city_id>/places',  methods=['GET', 'POST'], strict_slashes=False
)
def get_places_of_city_by_id(city_id):
    """Returns a JSON list of all HBnB places in a city."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    elif request.method == 'POST':
        post = request.get_json(silent=True)
        if post is None:
            return ("Not a JSON", 400)
        if type(post) is not dict:
            return ("Missing name", 400)
        name = post.get('name')
        if name is None:
            return ('Missing name', 400)
        user_id = post.get('user_id')
        if user_id is None:
            return ('Missing user_id', 400)
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        new_place = Place(name=name, state_id=city.id, user_id=user_id)
        new_place.save()
        return (jsonify(new_place.to_dict()), 201)


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE', 'GET', 'PUT'],
    strict_slashes=False
)
def get_place_by_id(place_id):
    """Returns JSON serialization of a place specified by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        place.delete()
        return ('{}', 200)
    elif request.method == 'PUT':
        # Get the update values
        post = request.get_json(silent=True)
        if post is None:
            return ('Not a JSON', 400)

        # Update the Place
        for key, value in post.items():
            # Ignore these reserved keys
            if key in ('id', 'created_at', 'updated_at', 'user_id', 'city_id'):
                continue
            setattr(place, key, value)
        place.save()

        return (jsonify(place.to_dict()), 200)
