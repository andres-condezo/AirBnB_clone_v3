#!/usr/bin/python3
"""
New view for Places objects that handles
all default RESTFul API actions.
"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def show_reviews(place_id):
    """ Retrieves the list of all Reviews objects from a Place """
    reviews_list = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review = storage.all('Review')
    for obj in review.values():
        objdict = obj.to_dict()
        if objdict['place_id'] == place_id:
            reviews_list.append(objdict)
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    req = request.get_json()

    if not req:
        abort(400, 'Not a JSON')
    if 'user_id' not in req:
        abort(400, 'Missing user_id')

    user = storage.get(User, req['user_id'])

    if user is None:
        abort(404)
    if 'text' not in req:
        abort(400, 'Missing text')
    else:
        req['place_id'] = place_id
        inst_review = Review(**req)
        storage.new(inst_review)
        storage.save()
        return make_response(jsonify(inst_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    put_data = request.get_json()
    if not put_data:
        abort(400, 'Not a JSON')

    for k, v in put_data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at',
                     'updated_at']:
            setattr(review, k, v)
    review.save()
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
