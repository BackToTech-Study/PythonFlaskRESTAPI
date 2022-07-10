import flask_injector
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from api.controler.value import value
from api.services.random_value_repository import RandomValueRepository
from database import database
from api.controler.status import status


def create_app(configuration_key='production'):
    app = Flask(__name__)

    if configuration_key == 'development':
        from test_configuration import TestConfiguration as Configuration
    else:
        from configuration import Configuration as Configuration

    app.config.from_object(Configuration())

    database.init_app(app)
    Migrate(app, database)

    app.register_blueprint(status, url_prefix='/status')
    app.register_blueprint(value, url_prefix='/value')

    def configure_dependencies(binder):
        binder.bind(RandomValueRepository, to=RandomValueRepository, scope=flask_injector.singleton)
        binder.bind(SQLAlchemy, to=database, scope=flask_injector.singleton)

    flask_injector.FlaskInjector(app=app, modules=[configure_dependencies])

    return app
