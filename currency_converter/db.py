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
    base = db.Column(db.String(50))
    quote = db.Column(db.String(50))
    rate = db.Column(db.Float)

    download = db.relationship('Download', backref=db.backref('fxrate', lazy=True))
    download_id = db.Column(db.Integer, db.ForeignKey('download.id'))

    def __repr__(self):
        return f'<FxRate (base {self.base}, quote {self.quote}, rate {self.rate}, download timestamp {self.download.timestamp})>'


class Download(db.Model):
    __tablename__ = "download"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f'<FxRate (id {self.id}, timestamp {self.download.timestamp})>'


def save_rates(timestamp, base_ccy, rates):
    download = Download(timestamp=timestamp)
    db.session.add(download)
    for quote_ccy, rate in rates.items():
        db.session.add(FxRate(base=base_ccy, quote=quote_ccy, rate=rate, download=download))
    db.session.commit()


def load_rates(rates):
    rates = [c.as_dict() for c in FxRate.query.all()]
    return rates






