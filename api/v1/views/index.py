#!/usr/bin/python3
"""
index.py module
"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status')
def status():
    """ returns a JSON """
    return jsonify({'status': 'OK'})
