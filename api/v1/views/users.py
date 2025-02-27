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
        if 'email' not in post:
            return ("Missing email", 400)
        if 'password' not in post:
            return ("Missing password", 400)
        if 'name' not in post:
            return ('Missing name', 400)

        new_user = User(
            name=post['name'], email=post['email'], password=post['password'])
        new_user.save()
        return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def get_user_from_id(user_id):
    """Returns a JSONified User specified by ID"""
    user = storage.get(User, user_id)
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
            if key in ('id', 'email', 'created_at', 'updated_at'):
                continue
            setattr(user, key, value)
        user.save()

        return (jsonify(user.to_dict()), 200)
