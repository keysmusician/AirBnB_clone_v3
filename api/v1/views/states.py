#!/usr/bin/python3
"""Creates index routes"""
from flask.globals import request
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def get_states():
    """Returns a JSON list of all states"""
    if request.method == 'GET':
        return jsonify(
            [state.to_dict() for state in storage.all(State).values()]
        )
    if request.method == 'POST':
        post = request.get_json()
        if post is None:
            return ('Not a JSON', 400)
        name = post.get('name')
        if name is None:
            return ('Missing name', 400)
        new_state = State(name=name)
        storage.new(new_state)
        return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<id>', methods=['DELETE', 'GET', 'PUT'])
def get_state_from_id(id):
    """Returns a JSONified State specified by ID"""
    state = storage.get("State", id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        return ('{}', 200)
    elif request.method == 'PUT':
        # Get the update values
        post = request.get_json()
        if post is None:
            return ('Not a JSON', 400)
        # Remove these reserved keys
        for key in ('id', 'created_at', 'updated_at'):
            post.pop(key, None)

        updated_State = State(state.to_dict().update(post))
        updated_State.save()

        return (jsonify(updated_State.to_dict()), 200)
