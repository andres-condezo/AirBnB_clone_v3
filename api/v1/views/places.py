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
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def show_places(city_id):
    """ Retrieves the list of all Place objects from a City """
    places_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = storage.all('Place')
    for obj in place.values():
        objdict = obj.to_dict()
        if objdict['city_id'] == city_id:
            places_list.append(objdict)
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    req = request.get_json()

    user = storage.get(User, req['user_id'])

    if not req:
        abort(400, 'Not a JSON')
    elif 'user_id' not in req:
        abort(400, 'Missing user_id')
    elif 'name' not in req:
        abort(400, 'Missing name')
    elif user is None:
        abort(404)
    else:
        """req['city_id'] = city_id
        req['user_id'] = user_id"""
        inst_place = Place(**req)
        storage.new(inst_place)
        storage.save()
        return make_response(jsonify(inst_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    put_data = request.get_json()
    if not put_data:
        abort(400, 'Not a JSON')

    for k, v in put_data.items():
        if k == 'name':
            setattr(place, k, v)
        else:
            continue
    place.save()
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
