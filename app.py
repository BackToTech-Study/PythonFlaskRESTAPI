import os

from flask import Flask

from api.controler.status import status


def create_app(configuration_key='production'):
    app = Flask(__name__)

    if configuration_key == 'development':
        from test_configuration import TestConfiguration as Configuration
    else:
        from configuration import Configuration as Configuration

    app.config.from_object(Configuration())
    app.register_blueprint(status, url_prefix='/status')

    return app
