from currency_converter.app import db

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


