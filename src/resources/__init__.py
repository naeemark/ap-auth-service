from flask_restful import Api
from src.resources.user import ChangePassword
from src.resources.user import TokenRefresh
from src.resources.user import UserLogin
from src.resources.user import UserRegister
from src.resources.user import UserLogout



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
    api.add_resource(TokenRefresh, "/auth/refresh")


    # Adding api-prefix for logging purposes
    app.config["API_PREFIX"] = api_prefix
