from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from os import environ

from resources.user import UserRegister, UserLogin
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI") or 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") or False
app.config['PROPAGATE_EXCEPTIONS'] = environ.get("PROPAGATE_EXCEPTIONS") or True
app.secret_key = environ.get("SECRET_KEY") or 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# no endpoint
jwt = JWTManager(app)

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
