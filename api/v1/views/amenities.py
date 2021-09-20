#!/usr/bin/python3
"""Creates cities view routes"""
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models import amenity
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_amenities():
    """Returns a JSON list of all amenities"""
    if request.method == 'GET':
        return jsonify(
            [Amenity.to_dict() for Amenity in storage.all(Amenity).values()]
        )
    if request.method == 'POST':
        post = request.get_json(silent=True)
        if post is None:
            return ("Not a JSON", 400)
        if type(post) is not dict:
            return ("Missing name", 400)
        name = post.get('name')
        if name is None:
            return ('Missing name', 400)
        new_amenity = Amenity(name=name)
        new_amenity.save()
        return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def get_amenity_from_id(id):
    """Returns a JSONified Amenity specified by ID"""
    amenity = storage.get("Amenity", id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        amenity.delete()
        return ('{}', 200)
    elif request.method == 'PUT':
        # Get the update values
        post = request.get_json(silent=True)
        if post is None:
            return ('Not a JSON', 400)

        # Update the Amenity
        for key, value in post.items():
            # Ignore these reserved keys
            if key in ('id', 'created_at', 'updated_at'):
                continue
            setattr(amenity, key, value)
        amenity.save()

        return (jsonify(amenity.to_dict()), 200)
