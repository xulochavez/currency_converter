from flask import Flask
from currency_converter.config import Config
from currency_converter import db


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_object(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)

    return app

