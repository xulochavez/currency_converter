import pytest
import datetime
from unittest import mock

from currency_converter import create_app
from currency_converter.config import TestConfig
from currency_converter.db import db
from currency_converter.currency_converter import CcyConverter


@pytest.fixture
def test_client():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()
        client = app.test_client()
        yield client
        db.drop_all()


@pytest.fixture()
def ccy_converter():
    ccy_converter = CcyConverter(timestamp=datetime.datetime.now(),
                                 base='USD',
                                 rates={'PLN': 4,
                                        'EUR': 2,
                                     })
    return ccy_converter


def test_convert(test_client, ccy_converter):
    with mock.patch('currency_converter.routes.get_ccy_converter', return_value=ccy_converter):
        response = test_client.get('/currency_converter/convert?from_ccy=PLN&to_ccy=EUR&amount=200')
        expected = {'amount': 200.0, 'converted_amount': 100, 'from_ccy': 'PLN', 'to_ccy': 'EUR'}
        actual = response.json
        assert expected == actual
