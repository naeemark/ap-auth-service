"""
  Flask App
"""
from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src import create_app
from src import db
from src.constant.exception import ValidationException
from src.resources.user import ChangePassword
from src.resources.user import TokenRefresh
from src.resources.user import UserLogin
from src.resources.user import UserRegister

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


@jwt.unauthorized_loader
def token_required(error):
    """
        Response for Authorization Exception
    """
    return jsonify({"message": ValidationException.AUTH, "error": error}), 401


@jwt.expired_token_loader
def token_expired(error):
    """
        Response for Token Expired Exception
    """
    return jsonify({"message": ValidationException.TOKEN_EXPIRED, "error": error}), 401


api = Api(app, "/{}/api/v1".format(app.config.get("STAGE")))
api.add_resource(UserRegister, "/user/register")
api.add_resource(UserLogin, "/user/login")
api.add_resource(TokenRefresh, "/auth/refresh")
api.add_resource(ChangePassword, "/user/changePassword")

# temporary logging
# list_routes = ["%s" % rule for rule in app.url_map.iter_rules()][0:-1]
# print("Routes:\n", "\n ".join(str(line) for line in list_routes))


if __name__ == "__main__":
    app.run()
