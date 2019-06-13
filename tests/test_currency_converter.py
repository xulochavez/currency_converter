
import datetime
import pytest

from currency_converter.currency_converter import CcyConverter, DataStaleError


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
    with pytest.raises(DataStaleError) as exc:
        stale_ccy_converter.convert(10, 'EUR', 'GBP')


