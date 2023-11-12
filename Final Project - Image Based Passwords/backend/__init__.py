from .models import users_database
from .login import login_manager
from flask_cors import CORS
from flask import Flask
import json
import os

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "config.json"

"""

    To run:
        export FLASK_APP="Final Project"
        flask run

"""
def create_app():
    app = Flask(__name__)
    CORS(app)

    config = None
    with open(os.path.join(PROJECT_DIR, CONFIG_FILE)) as f:
        config = json.load(f)

    app.config["SECRET_KEY"] = config["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    users_database.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        users_database.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
