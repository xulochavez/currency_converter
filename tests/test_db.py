import datetime
import pytest

from currency_converter import create_app
from currency_converter.config import TestConfig
from currency_converter.db import db, FxRate, save_rates, load_rates


@pytest.fixture
def test_app():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()


def test_save_rates(test_app):
    with test_app.app_context():
        download_timestamp = datetime.datetime.now()
        save_rates(base_ccy='USD', rates={'BRL': 4.1}, timestamp=download_timestamp)
        actual = FxRate.query.all()

        assert len(actual) == 1

        assert actual[0].download.base == 'USD'
        assert actual[0].download.timestamp == download_timestamp

        assert actual[0].quote == 'BRL'
        assert actual[0].rate == 4.1


def test_load_rates(test_app):
    with test_app.app_context():
        download_timestamp = datetime.datetime.now()
        save_rates(base_ccy='USD', rates={'BRL': 4.1}, timestamp=download_timestamp)
        download_timestamp_2 = datetime.datetime.now()
        save_rates(base_ccy='USD', rates={'BRL': 4.4}, timestamp=download_timestamp_2)
        base, rates, timestamp,  = load_rates()
        assert timestamp == download_timestamp_2
        assert base == 'USD'
        assert 'BRL' in rates
        assert rates['BRL'] == 4.4





