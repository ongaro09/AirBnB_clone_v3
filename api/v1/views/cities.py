#!/usr/bin/python3
"""City file"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request, Blueprint

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieve the list of all City objects of a State."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_a_city(city_id):
    """Retrieve a specific City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_city(city_id):
    """Delete a specific City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_a_city(state_id):
    """Create a new City object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    req['state_id'] = state_id
    new_city = City(**req)
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_a_city(city_id):
    """Update a specific City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for key in ['id', 'state_id', 'created_at', 'updated_at']:
        req.pop(key, None)
    for key, value in req.items():
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
