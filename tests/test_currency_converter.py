
import datetime
import pytest
from unittest import mock

from currency_converter.currency_converter import CcyConverter, DataStaleError, get_ccy_converter


@pytest.fixture
def fxrates_service_response_json():
    response_json = \
     {'disclaimer': 'Usage subject to terms: https://openexchangerates.org/terms',
     'license': 'https://openexchangerates.org/license', 'timestamp': 1560078008, 'base': 'USD',
     'rates': {'AED': 3.673014, 'AFN': 79.324827, 'ALL': 107.825, 'AMD': 479.11221, 'ANG': 1.874517, 'AOA': 336.676}}
    return response_json


@pytest.fixture()
def ccy_converter():
    ccy_converter = CcyConverter(timestamp=datetime.datetime.now(),
                                 base='USD',
                                 rates={'EUR': 0.8, 'GBP': 0.9})
    return ccy_converter


def test_convert(ccy_converter):
    expected_eur_to_gbp_rate = 0.9 / 0.8
    expected_amount = 10 * expected_eur_to_gbp_rate
    actual_amount = ccy_converter.convert(10, 'EUR', 'GBP')
    assert expected_amount == actual_amount


@pytest.fixture()
def stale_ccy_converter():
    stale_ccy_converter = CcyConverter(timestamp=datetime.datetime.now() - datetime.timedelta(2),
                                       base='USD',
                                       rates={'EUR': 0.8, 'GBP': 0.9})
    return stale_ccy_converter


def test_stale_rates(stale_ccy_converter):
    with pytest.raises(DataStaleError) as _exc:
        stale_ccy_converter.convert(10, 'EUR', 'GBP')


@mock.patch('currency_converter.currency_converter.fetch_and_save_rates')
@mock.patch('currency_converter.currency_converter.load_rates')
def test_get_ccy_converter_fetches_new_rates_if_stale(mock_load_rates, mock_fetch_and_save_rates):
    mock_load_rates.return_value = ('USD', {'EUR': 1}, datetime.datetime.now())
    mock_fetch_and_save_rates.return_value = ('USD', {'EUR': 1.1}, datetime.datetime.now())
    with mock.patch('currency_converter.currency_converter.CcyConverter.is_stale', return_value=True):
        _ = get_ccy_converter()

    assert mock_fetch_and_save_rates.call_count == 1






