import datetime
import logging
from flask import Flask
import pytest
from unittest import mock
from flask_sqlalchemy import SQLAlchemy

from currency_converter.db import save_rates


@pytest.fixture
def test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/currency_convertor_test.db'
    return app

@pytest.fixture
def test_db(test_app):
    db = SQLAlchemy(test_app)

    logging.info("creating db tables")
    db.create_all()
    yield db
    #db.drop_all()


def test_save_rates(test_db):
    import currency_converter.db
    with mock.patch.object(currency_converter.db, 'db', test_db):
        save_rates(timestamp=datetime.datetime.now(), base_ccy='USD', rates={'BRL': 4.1})



