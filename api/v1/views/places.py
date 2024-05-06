#!/usr/bin/python3
"""Handles RESTful API actions related to Place objects."""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieve the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_a_place(place_id):
    """Retrieve a specific Place object."""
    place = storage.get(Place, place_id)
    return jsonify((place.to_dict()) if place else abort(404))

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_place(place_id):
    """Delete a specific Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_a_place(city_id):
    """Create a new Place object."""
    city = storage.get(City, city_id)
    if city is None:
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
    if 'name' not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    req['city_id'] = city_id
    new_place = Place(**req)
    new_place.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_a_place(place_id):
    """Update a specific Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in req.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
