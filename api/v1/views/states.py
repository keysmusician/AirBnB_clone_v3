#!/usr/bin/python3
"""Creates states view routes"""
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """Returns a JSON list of all states"""
    if request.method == 'GET':
        return jsonify(
            [state.to_dict() for state in storage.all(State).values()]
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
        new_state = State(name=name)
        new_state.save()
        return (jsonify(new_state.to_dict()), 201)


@app_views.route(
    '/states/<id>', methods=['DELETE', 'GET', 'PUT'], strict_slashes=False)
def get_state_from_id(id):
    """Returns a JSONified State specified by ID"""
    state = storage.get(State, id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        return ('{}', 200)
    elif request.method == 'PUT':
        # Get the update values
        post = request.get_json(silent=True)
        if post is None:
            return ('Not a JSON', 400)

        # Update the State
        for key, value in post.items():
            # Ignore these reserved keys
            if key in ('id', 'created_at', 'updated_at'):
                continue
            setattr(state, key, value)
        state.save()

        return (jsonify(state.to_dict()), 200)
