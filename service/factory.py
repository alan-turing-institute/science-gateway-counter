from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from service.auth.api import UserApi
from service.database import db, ma

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Import environment specific variables from the supplied
    # configuration
    app.config.from_object("config.{}".format(config_name))

    # Load non-source controlled config variables from the instance folder
    # if present (fails silently if not present)
    app.config.from_pyfile("config.py", silent=True)

    # Load the URI stems from the base config
    from config.base import URI_STEMS

    api = Api(app)

    api.add_resource(UserApi, '/api/status')

    return app
