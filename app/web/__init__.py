from flask import Flask, g
from .views import frontend

flask_app = Flask('sleepy', template_folder='app/web/templates', static_folder='app/web/static')
flask_app.debug = True

flask_app.register_blueprint(frontend)
