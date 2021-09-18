#!/usr/bin/python3
"""
app.py module.
"""


from flask import Flask


app = Flask(__name__)


from os import getenv
from models import storage
from api.v1.views import app_views


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """ calls storage.close() """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
