#!/usr/bin/python3
"""Creates users view routes"""
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_users():
    """Returns a JSON list of all users"""
    if request.method == 'GET':
        return jsonify(
            [user.to_dict() for user in storage.all(User).values()])
    if request.method == 'POST':
        post = request.get_json(silent=True)
        if post is None:
            return ("Not a JSON", 400)
        if type(post) is not dict:
            return ("Missing name", 400)
        name = post.get('name')
        if name is None:
            return ('Missing name', 400)
        new_user = User(name=name)
        new_user.save()
        return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def get_user_from_id(id):
    """Returns a JSONified User specified by ID"""
    user = storage.get("User", id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        user.delete()
        return ('{}', 200)
    elif request.method == 'PUT':
        # Get the update values
        post = request.get_json(silent=True)
        if post is None:
            return ('Not a JSON', 400)

        # Update the User
        for key, value in post.items():
            # Ignore these reserved keys
            if key in ('id', 'created_at', 'updated_at'):
                continue
            setattr(user, key, value)
        user.save()

        return (jsonify(user.to_dict()), 200)
