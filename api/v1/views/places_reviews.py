#!/usr/bin/python3
"""Handles RESTful API actions related to Review objects."""
from flask import jsonify, abort, request, make_response, Blueprint
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve the list of all Review objects of a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_a_review(review_id):
    """Retrieve a specific Review object."""
    review = storage.get(Review, review_id)
    return jsonify((review.to_dict()) if review else abort(404))

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_review(review_id):
    """Delete a specific Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_a_review(place_id):
    """Create a new Review object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if not req:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user_id = req.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in req:
        return make_response(jsonify({"error": "Missing text"}), 400)
    req['place_id'] = place_id
    new_review = Review(**req)
    new_review.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_a_review(review_id):
    """Update a specific Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in req.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
