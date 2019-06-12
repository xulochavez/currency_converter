import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/currency_converter.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False