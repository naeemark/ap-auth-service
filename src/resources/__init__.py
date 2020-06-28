from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.resources.health import Health
from src.resources.session import RefreshSession
from src.resources.session import ValidateSession
from src.resources.user.change_password import ChangePassword
from src.resources.user.login import LoginUser
from src.resources.user.logout import LogoutUser
from src.resources.user.register import RegisterUser
from src.utils.blacklist_manager import BlacklistManager
from src.utils.constant.response_messages import FRESH_TOKEN
from src.utils.constant.response_messages import TOKEN_EXPIRED
from src.utils.constant.response_messages import TOKEN_REVOKED
from src.utils.response_builder import get_error_response


def initialize_jwt_manager(app):
    """
        Intialized JWT Manager
        - Registers overridden callbacks for custom response
    """

    jwt_manager = JWTManager(app)

    @jwt_manager.needs_fresh_token_loader
    def fresh_token_required():
        return get_error_response(status_code=401, message=FRESH_TOKEN)

    @jwt_manager.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return decrypted_token["jti"] in BlacklistManager().get_jti_list()

    @jwt_manager.revoked_token_loader
    def revoke_token_callback():
        return get_error_response(status_code=401, message=TOKEN_REVOKED)

    @jwt_manager.expired_token_loader
    def expired_token_callback():
        return get_error_response(status_code=401, message=TOKEN_EXPIRED)

    @jwt_manager.unauthorized_loader
    def unauthorized_loader_callback(reason):
        return get_error_response(status_code=401, message=reason)

    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error_reason):
        return get_error_response(status_code=422, message=error_reason)


def initialize_resources(app):
    if not app:
        return

    initialize_jwt_manager(app)

    BlacklistManager.initialize_redis(app_config=app.config)

    api_prefix = "/api/v1"

    # Instantiates API
    api = Api(app=app, prefix=api_prefix)

    # Adds resources for Health Check
    api.add_resource(Health, "/health")

    # Adds resources for User Entity
    api.add_resource(RegisterUser, "/user/register")
    api.add_resource(LoginUser, "/user/login")
    api.add_resource(ChangePassword, "/user/changePassword")
    api.add_resource(LogoutUser, "/user/logout")

    # Adds resources for Auth Entity
    api.add_resource(RefreshSession, "/session/refresh")
    api.add_resource(ValidateSession, "/session/validate")

    # Adding api-prefix for logging purposes
    app.config["API_PREFIX"] = api_prefix
