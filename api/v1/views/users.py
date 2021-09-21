#!/usr/bin/python3
"""
New view for User objects that handles
all default RESTFul API actions.
"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def show_users():
    """ Retrieves the list of all User objects """
    users_list = []
    all_users = storage.all('User')
    for obj in all_users.values():
        users_list.append(obj.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes an User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates an User """
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    if 'email' not in req:
        abort(400, 'Missing email')
    if 'password' not in req:
        abort(400, 'Missing password')
    inst_user = User(**req)
    storage.save()
    return make_response(jsonify(inst_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_usermenity(user_id):
    """ Updates an User object """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    put_data = request.get_json()
    if not put_data:
        abort(400, 'Not a JSON')

    for k, v in put_data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
        else:
            continue
    user.save()
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
