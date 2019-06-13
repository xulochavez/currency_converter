import datetime
import pytest

from currency_converter import create_app
from currency_converter.config import TestConfig
from currency_converter.db import db, save_rates, FxRate


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
        save_rates(timestamp=download_timestamp, base_ccy='USD', rates={'BRL': 4.1})
        actual = FxRate.query.all()
        assert len(actual) == 1
        assert actual[0].base == 'USD'
        assert actual[0].quote == 'BRL'
        assert actual[0].rate == 4.1
        assert actual[0].download.timestamp == download_timestamp




