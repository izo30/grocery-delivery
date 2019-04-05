# create application
from flask import Flask
import os

from instance.config import app_config
from instance.db_config import DbSetup


def create_app(config):

    app = Flask(__name__)

    from .api import version1 as v1
    app.register_blueprint(v1)
    app.config.from_object(app_config[config])
    app.url_map.strict_slashes = False

    return app
