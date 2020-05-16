from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)

    return app
