from flask_restful import Api
from src.constant.error_handler import ErrorHandler
from src.constant.exception import ValidationException
from src.resources.auth import RevokeAccess
from src.resources.auth import StartSession
from src.resources.auth import TokenRefresh
from src.resources.user import ChangePassword
from src.resources.user import UserLogin
from src.resources.user import UserLogout
from src.resources.user import UserRegister
from src.utils.blacklist import BlacklistManager
from src.utils.errors import error_handler


class InitializationJWT:
    exception = error_handler.exception_factory("Auth")

    @classmethod
    def initialize(cls, jwt_instance):
        cls.initialize_token_in_blacklist_loader(jwt_instance)
        cls.initialize_invalid_token(jwt_instance)
        cls.initialize_expired_token_callback(jwt_instance)
        cls.initialize_revoke_token_callback(jwt_instance)
        cls.initialize_fresh_token_required(jwt_instance)

    @classmethod
    def initialize_fresh_token_required(cls, jwt):
        @jwt.needs_fresh_token_loader
        def fresh_token_required():
            """
            response for fresh token required
            """
            return cls.exception.get_response(
                ErrorHandler.FRESH_TOKEN, jsonify_response=True
            )

        return fresh_token_required

    @classmethod
    def initialize_token_in_blacklist_loader(cls, jwt):
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

    @classmethod
    def initialize_revoke_token_callback(cls, jwt):
        @jwt.revoked_token_loader
        def revoke_token_callback():
            """token revoke response handled"""

            return cls.exception.get_response(
                ErrorHandler.TOKEN_REVOKED, jsonify_response=True
            )

        return revoke_token_callback

    @classmethod
    def initialize_expired_token_callback(cls, jwt):
        @jwt.expired_token_loader
        def expired_token_callback():
            """token expire response handled"""
            return cls.exception.get_response(
                ErrorHandler.TOKEN_EXPIRED, jsonify_response=True
            )

        return expired_token_callback

    @classmethod
    def initialize_invalid_token(cls, jwt):
        @jwt.invalid_token_loader
        def invalid_token_callback(error_reason):
            """invalid token response handled"""
            ValidationException.TOKEN_INVALID = error_reason
            return cls.exception.get_response(
                ErrorHandler.TOKEN_INVALID,
                status=422,
                error_description=error_reason,
                jsonify_response=True,
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
