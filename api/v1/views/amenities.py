#!/usr/bin/python3
"""Handles RESTful API actions related to Amenity objects."""
from flask import jsonify, abort, request, Blueprint
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieve the list of all Amenity objects."""
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_an_amenity(amenity_id):
    """Retrieve a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_an_amenity(amenity_id):
    """Delete a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_an_amenity():
    """Create a new Amenity object."""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    new_amenity = Amenity(**req)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_an_amenity(amenity_id):
    """Update a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for key in ['id', 'created_at', 'updated_at']:
        req.pop(key, None)
    for key, value in req.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
