import datetime
import os

from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.resources.session import RefreshSession
from src.resources.session import RevokeSession
from src.resources.session import StartSession
from src.resources.user import ChangePassword
from src.resources.user import UserLogin
from src.resources.user import UserLogout
from src.resources.user import UserRegister
from src.utils.blacklist_manager import BlacklistManager
from src.utils.constant.response_messages import FRESH_TOKEN
from src.utils.constant.response_messages import TOKEN_EXPIRED
from src.utils.constant.response_messages import TOKEN_REVOKED
from src.utils.errors import error_handler
from src.utils.response_builder import get_error_response


class InitializationJWT:
    exception = error_handler.exception_factory("Auth")

    @classmethod
    def initialize(cls, jwt_instance):
        cls.initialize_token_in_blacklist_loader(jwt_instance)
        cls.initialize_invalid_token(jwt_instance)
        cls.initialize_expired_token_callback(jwt_instance)
        cls.initialize_revoke_token_callback(jwt_instance)
        cls.initialize_fresh_token_required(jwt_instance)
        cls.initialize_unauthorized_loader_callback(jwt_instance)

    @classmethod
    def initialize_fresh_token_required(cls, jwt):
        @jwt.needs_fresh_token_loader
        def fresh_token_required():
            """
            response for fresh token required
            """
            return get_error_response(status_code=401, message=FRESH_TOKEN)

        return fresh_token_required

    @classmethod
    def initialize_token_in_blacklist_loader(cls, jwt):
        """call back for blacklist tokens"""

        @jwt.token_in_blacklist_loader
        def check_if_token_in_blacklist(decrypted_token):
            """
            this method will check if a token is blacklisted
            """
            return decrypted_token["jti"] in BlacklistManager().get_jti_list()  # Here we blacklist particular users.

        return check_if_token_in_blacklist

    @classmethod
    def initialize_revoke_token_callback(cls, jwt):
        @jwt.revoked_token_loader
        def revoke_token_callback():
            """token revoke response handled"""
            return get_error_response(status_code=401, message=TOKEN_REVOKED)

        return revoke_token_callback

    @classmethod
    def initialize_expired_token_callback(cls, jwt):
        @jwt.expired_token_loader
        def expired_token_callback():
            """token expire response handled"""
            return get_error_response(status_code=401, message=TOKEN_EXPIRED)

        return expired_token_callback

    @classmethod
    def initialize_unauthorized_loader_callback(cls, jwt):
        @jwt.unauthorized_loader
        def unauthorized_loader_callback(reason):
            """missing token response handled"""

            return get_error_response(status_code=401, message=reason)

        return unauthorized_loader_callback

    @classmethod
    def initialize_invalid_token(cls, jwt):
        @jwt.invalid_token_loader
        def invalid_token_callback(error_reason):
            """invalid token response handled"""

            return get_error_response(status_code=422, message=error_reason)

        return invalid_token_callback


def initialize_resources(app, redis_instance):
    jwt = JWTManager(app)

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
        minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"])
    )
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=int(os.environ["JWT_REFRESH_TOKEN_EXPIRES_DAYS"]))
    token_expire_seconds = app.config["JWT_ACCESS_TOKEN_EXPIRES"].seconds
    BlacklistManager().initialize_redis(token_expire_seconds, redis_instance)
    InitializationJWT.initialize(jwt)
    api_prefix = "/api/v1"

    # Instantiates API
    api = Api(app=app, prefix=api_prefix)

    # Adds resources for User Entity
    api.add_resource(UserRegister, "/user/register")
    api.add_resource(UserLogin, "/user/login")
    api.add_resource(ChangePassword, "/user/changePassword")
    api.add_resource(UserLogout, "/user/logout")

    # Adds resources for Auth Entity
    api.add_resource(StartSession, "/session/start")
    api.add_resource(RefreshSession, "/session/refresh")
    api.add_resource(RevokeSession, "/session/revoke")

    # Adding api-prefix for logging purposes
    app.config["API_PREFIX"] = api_prefix
