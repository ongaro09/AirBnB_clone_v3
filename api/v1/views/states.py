#!/usr/bin/python3
"""States object file"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, Blueprint, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """This function returns a list of all states"""
    list_of_all_states = []
    states = storage.all(State).values()
    for state in states:
        list_of_all_states.append(state.to_dict())
    return jsonify(lizt)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id):
    """This function finds a unique state based on a unique identifier"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    returned_value = state.to_dict()
    return jsonify(returned_value)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_state(state_id):
    """ This function deletes a specific State"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_a_state():
    """This function creates a state"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    key = 'name'
    if key not in req:
        abort(400, "Missing name")
    new_state = State(**req)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_a_state(state_id):
    """ the function of this method is to update a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_val = request.get_json()
    if request_val is None:
        abort(400, "Not a JSON")
    for k, value in request_val.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, value)
    storage.save()
    return jsonify(state.to_dict()), 200
