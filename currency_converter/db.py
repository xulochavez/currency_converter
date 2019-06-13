import click

from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')


def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)


class FxRate(db.Model):
    __tablename__ = "fxrate"
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(50))
    rate = db.Column(db.Float)

    download = db.relationship('Download', backref=db.backref('fxrate', lazy=True))
    download_id = db.Column(db.Integer, db.ForeignKey('download.id'))

    def __repr__(self):
        return f'<FxRate (quote {self.quote}, rate {self.rate}, download timestamp {self.download.timestamp})>'


class Download(db.Model):
    __tablename__ = "download"
    id = db.Column(db.Integer, primary_key=True)
    base = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f'<FxRate (id {self.id}, base {self.base}, timestamp {self.download.timestamp})>'


def save_rates(base_ccy, rates, timestamp):
    download = Download(timestamp=timestamp, base=base_ccy)
    db.session.add(download)
    for quote_ccy, rate in rates.items():
        db.session.add(FxRate(quote=quote_ccy, rate=rate, download=download))
    db.session.commit()


def load_rates():
    downloads = Download.query.order_by(Download.timestamp).all()
    if not downloads:
        return None, {}, None

    latest_download = downloads[-1]
    rate_objs = FxRate.query.filter(FxRate.download==latest_download).all()
    base, timestamp = latest_download.base, latest_download.timestamp
    rates = {r.quote: r.rate for r in rate_objs}
    return base, rates, timestamp






