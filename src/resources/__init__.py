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


def initialize_token_in_blacklist_loader(jwt):
    """call back for blacklist tokens"""

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """
        this method will check if a token is blacklisted
        """
        return decrypted_token["jti"] in BlacklistManager().get_jti_list()

    return check_if_token_in_blacklist


def initialize_resources(app, redis_instance):
    jwt = JWTManager(app)

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
        minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"])
    )
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=int(os.environ["JWT_REFRESH_TOKEN_EXPIRES_DAYS"]))
    token_expire_seconds = app.config["JWT_ACCESS_TOKEN_EXPIRES"].seconds
    BlacklistManager().initialize_redis(token_expire_seconds, redis_instance)
    initialize_token_in_blacklist_loader(jwt)
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
