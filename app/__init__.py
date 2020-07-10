import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from config import Config
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, users, songs, albums, creators
