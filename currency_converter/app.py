from flask import Flask, jsonify

import click

from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/currency_convertor.db'
db = SQLAlchemy(app)


# WARNING putting the code just below in db.py would lead to a circular import (through the db obj)
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')


app.cli.add_command(init_db_command)


@app.route("/")
def index():
    return "Welcome to the currency convertor app"


def get_ccy_converter():
    pass


@app.route('/currency_convertor/rates', methods=['GET'])
def get_rates():
    rates = [c.as_dict() for c in FxRate.query.all()]
    return jsonify(rates)


