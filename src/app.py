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
from src.resources.user import UserLogout
from src.utils.blacklist import BlacklistManager

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


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BlacklistManager().get_jti_list()  # Here we blacklist particular users.


api = Api(app, "/{}/api/v1".format(app.config.get("STAGE")))
api.add_resource(UserRegister, "/user/register")
api.add_resource(UserLogin, "/user/login")
api.add_resource(TokenRefresh, "/auth/refresh")
api.add_resource(ChangePassword, "/user/changePassword")
api.add_resource(UserLogout, "/user/logout")

# temporary logging
# list_routes = ["%s" % rule for rule in app.url_map.iter_rules()][0:-1]
# print("Routes:\n", "\n ".join(str(line) for line in list_routes))


if __name__ == "__main__":
    app.run()
