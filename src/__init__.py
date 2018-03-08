from .config import app_config
from flask import Flask
from .views import app


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.register_blueprint(app)
    return app
