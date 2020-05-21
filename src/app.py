"""
  Flask App
"""
from flask import jsonify
from flask_jwt_extended import JWTManager
from src import create_app
from src import db
from src.constant.exception import ValidationException
from src.resources import initialize_resources
from src.utils.blacklist import BlacklistManager

app = create_app("flask.cfg")


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


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BlacklistManager().get_jti_list()  # Here we blacklist particular users.


initialize_resources(app)

if __name__ == "__main__":
    app.run()