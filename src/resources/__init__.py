from flask_restful import Api
from src.resources.auth import StartSession
from src.resources.auth import TokenRefresh
from src.resources.user import ChangePassword
from src.resources.user import UserLogin
from src.resources.user import UserRegister


def initialize_resources(app):
    api_prefix = "/{}/api/v1".format(app.config.get("STAGE"))

    # Instantiates API
    api = Api(app=app, prefix=api_prefix)

    # Adds resources for User Entity
    api.add_resource(UserRegister, "/user/register")
    api.add_resource(UserLogin, "/user/login")
    api.add_resource(ChangePassword, "/user/changePassword")

    # Adds resources for Auth Entity
    api.add_resource(TokenRefresh, "/auth/refreshToken")
    api.add_resource(StartSession, "/auth/startSession")

    # Adding api-prefix for logging purposes
    app.config["API_PREFIX"] = api_prefix
