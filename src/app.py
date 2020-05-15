from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, APISpec

from src.resources.user import (UserRegister,
                            UserLogin,
                            TokenRefresh,
                            ChangePassword)
from src.db import db
from src.constant.exception import Exception

POSTGRES_URL = environ.get("POSTGRES_URL") or "127.0.0.1:5432"
POSTGRES_USER = environ.get("POSTGRES_USER") or "postgres"
POSTGRES_PW = environ.get("POSTGRES_PW") or "test123"
POSTGRES_DB = environ.get("POSTGRES_DB") or "postgres"

DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                      db=POSTGRES_DB)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") or False
app.config['PROPAGATE_EXCEPTIONS'] = environ.get("PROPAGATE_EXCEPTIONS") or True
app.secret_key = environ.get("SECRET_KEY") or 'jose'
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'ALETHEA',
    'uiversion': 3,
    'description':'',
    'version':"1.0"
}

swagger = Swagger(app)


@app.before_first_request
def create_tables():
    db.create_all()


# no endpoint
jwt = JWTManager(app)


@jwt.unauthorized_loader
def token_required(error):
    return jsonify(
        {
            "message": Exception.AUTH
        }), 401


@jwt.expired_token_loader
def token_expired(error):
    return jsonify(
        {
            "message": Exception.TOKEN_EXPIRED
        }), 401


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ChangePassword, '/change-password')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
