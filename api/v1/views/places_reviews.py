#!/usr/bin/python3
"""Creates reviews view routes"""
from api.v1.views import app_views
from flask import abort, jsonify
from flask.globals import request
from models import storage
from models.review import Review


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET', 'POST'],
    strict_slashes=False
)
def get_reviews_of_place_by_id(place_id):
    """
    GET: Returns a JSON list of all reviews of places in a city
    POST: Creates and returns new Place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([review.to_dict() for review in place.reviews])

    elif request.method == 'POST':
        post = request.get_json(silent=True)
        if post is None:
            return ("Not a JSON", 400)
        if type(post) is not dict:
            return ("Missing text", 400)
        text = post.get('text')
        if text is None:
            return ('Missing text', 400)
        user_id = post.get('user_id')
        if user_id is None:
            return ('Missing user_id', 400)
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        new_review = Review(name=text, state_id=place.id, user_id=user_id)
        new_review.save()
        return (jsonify(new_review.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE', 'GET', 'PUT'],
    strict_slashes=False
)
def get_place_by_id(review_id):
    """
    DELETE: Deletes a Review specified by review_id
    GET: Returns a JSON serialization of a Review specified by review_id
    PUT: Updates and returns a Review specified by review_id
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        review.delete()
        return ('{}', 200)
    elif request.method == 'PUT':
        # Get the update values
        post = request.get_json(silent=True)
        if post is None:
            return ('Not a JSON', 400)

        # Update the Review
        for key, value in post.items():
            # Ignore these reserved keys
            if key in (
                'id', 'created_at', 'updated_at', 'user_id', 'place_id'
            ):
                continue
            setattr(review, key, value)
        review.save()

        return (jsonify(review.to_dict()), 200)
