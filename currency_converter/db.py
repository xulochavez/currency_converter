from currency_converter.models import FxRate, Download, db


def save_rates(timestamp, base_ccy, rates):
    db.session.add(Download(timestamp=timestamp))
    for quote_ccy, rate in rates.items():
        db.session.add(FxRate(base=base_ccy, quote=quote_ccy, rate=rate))
    db.session.commit()


def load_rates(rates):
    rates = [c.as_dict() for c in FxRate.query.all()]
    return rates


