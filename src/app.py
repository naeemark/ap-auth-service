"""
  Flask App
"""
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src import create_app
from src import db
from src.resources.user import ChangePassword
from src.resources.auth import TokenRefresh
from src.resources.user import UserLogin
from src.resources.user import UserRegister
from src.resources.auth import startSession

app = create_app("flask.cfg")


@app.before_first_request
def create_tables():
    """
       Initialize Database
    """
    db.create_all()


# no endpoint
jwt = JWTManager(app)

api = Api(app, "/{}/api/v1".format(app.config.get("STAGE")))
api.add_resource(UserRegister, "/user/register")
api.add_resource(UserLogin, "/user/login")
api.add_resource(TokenRefresh, "/auth/refresh")
api.add_resource(ChangePassword, "/user/changePassword")
api.add_resource(startSession, "/auth/StartSession")

# temporary logging
# list_routes = ["%s" % rule for rule in app.url_map.iter_rules()][0:-1]
# print("Routes:\n", "\n ".join(str(line) for line in list_routes))


if __name__ == "__main__":
    db.init_app(app)
    app.run()
