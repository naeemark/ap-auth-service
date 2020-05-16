"""
  Flask App Launcher
"""
import os
import pathlib

from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.constant.exception import ValidationException
from src.db import db
from src.resources.user import ChangePassword
from src.resources.user import TokenRefresh
from src.resources.user import UserLogin
from src.resources.user import UserRegister

project_folder = pathlib.Path(__file__).parent.absolute()
load_dotenv(os.path.join(project_folder, ".env"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS"
)
app.config["PROPAGATE_EXCEPTIONS"] = os.getenv("PROPAGATE_EXCEPTIONS")
app.secret_key = os.getenv("SECRET_KEY")

api = Api(app)


@app.before_first_request
def create_tables():
    """
       Initialize Database
    """
    db.init_app(app)
    db.create_all()


# no endpoint
jwt = JWTManager(app)


@jwt.unauthorized_loader
def token_required(error):
    """
        Response for Authorization Exception
    """
    return jsonify({"message": ValidationException.AUTH, "error": error}), 401


@jwt.expired_token_loader
def token_expired(error):
    """
        Response for Token Expired Exception
    """
    return jsonify({"message": ValidationException.TOKEN_EXPIRED, "error": error}), 401


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(ChangePassword, "/change-password")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
