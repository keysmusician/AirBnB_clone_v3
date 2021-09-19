#!/usr/bin/python3
"""Flask app"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes the storage engine"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Returns a JSON format 404"""
    return (jsonify(error="Not found"), 404)


if __name__ == '__main__':
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', '5000')
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host=host, port=port, threaded=True)
