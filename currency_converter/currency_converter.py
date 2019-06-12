import datetime


class DataStaleError(Exception):
    pass


class CcyConverter:

    def __init__(self, usd_rates, timestamp):
        self.usd_rates = usd_rates
        self.timestamp = timestamp

    def convert(self, from_ccy_amount, from_ccy, to_ccy):
        if self.is_stale():
            raise DataStaleError()
        if from_ccy not in self.usd_rates:
            raise KeyError(f'currency {from_ccy} not found')
        elif to_ccy not in self.usd_rates:
            raise KeyError(f'currency {to_ccy} not found')
        usd_amount = from_ccy_amount / self.usd_rates.get(from_ccy)
        return usd_amount * self.usd_rates.get(to_ccy)

    def is_stale(self):
        """True if rates timestamp is older than 24h"""
        return self.timestamp < datetime.datetime.now() - datetime.timedelta(1)