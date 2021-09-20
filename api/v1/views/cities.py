#!/usr/bin/python3
"""
New view for State objects that handles
all default RESTFul API actions.
"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def show_cities(state_id):
    """ Retrieves the list of all City objects from a State """
    cities_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = storage.all('City')
    for obj in city.values():
        objdict = obj.to_dict()
        if objdict['state_id'] == state_id:
            cities_list.append(objdict)
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a City """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    elif 'name' not in req:
        abort(400, 'Missing name')
    else:
        req['state_id'] = state_id
        inst_city = City(**req)
        storage.new(inst_city)
        storage.save()
        return make_response(jsonify(inst_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    put_data = request.get_json()
    if not put_data:
        abort(400, 'Not a JSON')

    for k, v in put_data.items():
        if k == 'name':
            setattr(city, k, v)
        else:
            continue
    city.save()
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
