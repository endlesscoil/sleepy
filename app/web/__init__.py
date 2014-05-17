from flask import Flask, g
from .views import frontend
from ..db import db

flask_app = Flask('sleepy', template_folder='app/web/templates', static_folder='app/web/static')
flask_app.debug = True
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleepy.db'

db.init_app(flask_app)

flask_app.register_blueprint(frontend)
