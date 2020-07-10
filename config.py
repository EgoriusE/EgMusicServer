import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:9368@localhost/EgMusic'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
