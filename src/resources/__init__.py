from flask_restful import Api
from src.resources.user import ChangePassword
from src.resources.user import TokenRefresh
from src.resources.user import UserLogin
from src.resources.user import UserRegister


def initialize_resources(app):
    # Instantiates API
    api = Api(app, "/{}/api/v1".format(app.config.get("STAGE")))

    # Adds resources for User Entity
    api.add_resource(UserRegister, "/user/register")
    api.add_resource(UserLogin, "/user/login")
    api.add_resource(ChangePassword, "/user/changePassword")

    # Adds resources for Auth Entity
    api.add_resource(TokenRefresh, "/auth/refresh")
