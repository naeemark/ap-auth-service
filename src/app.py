"""
  Flask App
"""
import os

import redis
from flask import jsonify
from flask_jwt_extended import JWTManager
from src import create_app
from src import db
from src.constant.error_code import ErrorCode
from src.constant.exception import ValidationException
from src.constant.rules import get_error_response as response
from src.resources import initialize_resources
from src.resources import initialize_token_in_blacklist_loader
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


@jwt.revoked_token_loader
def revoke_token_callback():
    """token revoke response handled"""
    return (
        jsonify(
            {
                "responseMessage": "Auth error",
                "responseCode": 401,
                "response": response("Token Revoked", "AUTH_ERROR"),
            }
        ),
        401,
    )


@jwt.expired_token_loader
def expired_token_callback():
    """token expire response handled"""
    return (
        jsonify(
            {
                "responseMessage": "Auth error",
                "responseCode": 401,
                "response": response(ErrorCode.TOKEN_EXPIRED, "AUTH_ERROR"),
            }
        ),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error_reason):
    """invalid token response handled"""
    ValidationException.TOKEN_INVALID = error_reason
    return (
        jsonify(
            {
                "responseMessage": "Auth error",
                "responseCode": 422,
                "response": response(ErrorCode.TOKEN_INVALID, "AUTH_ERROR"),
            }
        ),
        422,
    )


redis_instance = redis.Redis(
    host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"]
)
BlacklistManager().initialize_redis(app, redis_instance)
initialize_token_in_blacklist_loader(jwt)
initialize_resources(app)

if __name__ == "__main__":
    app.run()
