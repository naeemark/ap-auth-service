from flask import jsonify
from flask_restful import Api
from src.constant.error_code import ErrorCode
from src.constant.exception import ValidationException
from src.constant.rules import get_error_response as response
from src.resources.auth import RevokeAccess
from src.resources.auth import StartSession
from src.resources.auth import TokenRefresh
from src.resources.user import ChangePassword
from src.resources.user import UserLogin
from src.resources.user import UserLogout
from src.resources.user import UserRegister
from src.utils.blacklist import BlacklistManager


def initialize_token_in_blacklist_loader(jwt):
    """call back for blacklist tokens"""

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """
        this method will check if a token is blacklisted
        """
        return (
            decrypted_token["jti"] in BlacklistManager().get_jti_list()
        )  # Here we blacklist particular users.

    return check_if_token_in_blacklist


def initialize_revoke_token_callback(jwt):
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

    return revoke_token_callback


def initialize_expired_token_callback(jwt):
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

    return expired_token_callback


def initialize_invalid_token(jwt):
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

    return invalid_token_callback


def initialize_resources(app):
    api_prefix = "/{}/api/v1".format(app.config.get("STAGE"))

    # Instantiates API
    api = Api(app=app, prefix=api_prefix)

    # Adds resources for User Entity
    api.add_resource(UserRegister, "/user/register")
    api.add_resource(UserLogin, "/user/login")
    api.add_resource(ChangePassword, "/user/changePassword")
    api.add_resource(UserLogout, "/user/logout")

    # Adds resources for Auth Entity
    api.add_resource(TokenRefresh, "/auth/refreshToken")
    api.add_resource(StartSession, "/auth/startSession")
    api.add_resource(RevokeAccess, "/auth/revokeAccess")

    # Adding api-prefix for logging purposes
    app.config["API_PREFIX"] = api_prefix
