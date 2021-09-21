#!/usr/bin/python3
"""
app.py module.
"""


from flask import Flask, make_response, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """ calls storage.close() """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns a JSON-formatted 404 status code response """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
