#!/usr/bin/python3
"""
New view for State objects that handles
all default RESTFul API actions.
"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def show_states():
    """ Retrieves the list of all State objects """
    states_list = []
    all_states = storage.all('State')
    for obj in all_states.values():
        states_list.append(obj.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    elif 'name' not in req:
        abort(400, 'Missing name')
    else:
        inst_state = State(**req)
        storage.new(inst_state)
        storage.save()
        return make_response(jsonify(inst_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    put_data = request.get_json()
    if not put_data:
        abort(400, 'Not a JSON')

    for k, v in put_data.items():
        if k == 'name':
            setattr(state, k, v)
        else:
            continue
    state.save()
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
