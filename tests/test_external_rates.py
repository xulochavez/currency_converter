import requests
import datetime
from unittest import mock
import pytest

from currency_converter.external_rates import fetch_rates


@pytest.fixture
def fxrates_service_response_json():
    response_json = \
     {'disclaimer': 'Usage subject to terms: https://openexchangerates.org/terms',
     'license': 'https://openexchangerates.org/license', 'timestamp': 1560078008, 'base': 'USD',
     'rates': {'AED': 3.673014, 'AFN': 79.324827, 'ALL': 107.825, 'AMD': 479.11221, 'ANG': 1.874517, 'AOA': 336.676}}
    return response_json


@mock.patch('currency_converter.external_rates.requests.get')
def test_fetch_rates(mock_get, fxrates_service_response_json):
    mock_response = mock.Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.return_value = fxrates_service_response_json
    mock_get.return_value = mock_response
    timestamp, rates = fetch_rates()
    assert timestamp == datetime.datetime(2019, 6, 9, 12, 0, 8)
    assert isinstance(rates, dict)
    assert rates['AED'] == 3.673014