from flask_restful import Api
from src.resources.auth import RevokeAccess
from src.resources.auth import StartSession
from src.resources.auth import TokenRefresh
from src.resources.user import ChangePassword
from src.resources.user import UserLogin
from src.resources.user import UserLogout
from src.resources.user import UserRegister
from src.utils.blacklist import BlacklistManager


def initialize_resources(app, jwt):
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """
        :param decrypted_token: token dict
        :return: this method will check if a token is blacklisted
        and will be called automatically when blacklist is enabled
        """
        return (
            decrypted_token["jti"] in BlacklistManager().get_jti_list()
        )  # Here we blacklist particular users.

    if "BlacklistManager" not in check_if_token_in_blacklist.__code__.co_names:
        raise ValueError("expected BlacklistManager list")

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
