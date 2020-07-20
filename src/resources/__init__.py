from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.resources.analysis_profile import AnalysisProfile
from src.resources.common import is_token_blacklisted
from src.resources.health import Health
from src.resources.session import RefreshSession
from src.resources.session import ValidateSession
from src.resources.user.admin import ApproveAnalysisProfile
from src.resources.user.admin import ApproveUser
from src.resources.user.admin import DeleteAnalysisProfileById
from src.resources.user.admin import GetAnalysisProfileById
from src.resources.user.admin import GetAnalysisProfiles
from src.resources.user.admin import GetUserByEmail
from src.resources.user.admin import GetUsers
from src.resources.user.admin import ToggelAnalysisProfileStatus
from src.resources.user.admin import ToggelUserAccess
from src.resources.user.change_password import ChangePassword
from src.resources.user.get_user import GetUser
from src.resources.user.init_reset_password import InitResetPassword
from src.resources.user.init_verify_email import InitVerifyEmail
from src.resources.user.login import LoginUser
from src.resources.user.logout import LogoutUser
from src.resources.user.register import RegisterUser
from src.resources.user.reset_password import ResetPassword
from src.resources.user.verify_email import VerifyEmail
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
        return get_error_response(status_code=401, message=TOKEN_REVOKED)

    @jwt_manager.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return is_token_blacklisted(decrypted_token)

    @jwt_manager.revoked_token_loader
    def revoke_token_callback():
        return get_error_response(status_code=401, message=TOKEN_REVOKED)

    @jwt_manager.expired_token_loader
    def expired_token_callback():
        return get_error_response(status_code=401, message=TOKEN_REVOKED)

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

    api_prefix = "/api/auth"

    # Allow Origins
    CORS(app, resources={r"*": {"origins": "*"}})

    # Instantiates API
    api = Api(app=app, prefix=api_prefix)

    # Adds resources for Health Check
    api.add_resource(Health, "/health")

    # Adds resources for User Entity
    api.add_resource(RegisterUser, "/v1/user/register")
    api.add_resource(LoginUser, "/v1/user/login")
    api.add_resource(ChangePassword, "/v1/user/changePassword")
    api.add_resource(LogoutUser, "/v1/user/logout")
    api.add_resource(GetUser, "/v1/user")

    # Adds resources for Auth Entity
    api.add_resource(InitResetPassword, "/v1/user/initResetPassword")
    api.add_resource(ResetPassword, "/v1/user/resetPassword")
    api.add_resource(InitVerifyEmail, "/v1/user/initVerifyEmail")
    api.add_resource(VerifyEmail, "/v1/user/verifyEmail")

    # Adds resources for Analysis Profile
    api.add_resource(AnalysisProfile, "/v1/analysisProfile")

    # Adds Admin API Endpoints for Users
    api.add_resource(GetUsers, "/v1/admin/users")
    api.add_resource(GetUserByEmail, "/v1/admin/users/<email>")
    api.add_resource(ApproveUser, "/v1/admin/users/<email>/approve")
    api.add_resource(ToggelUserAccess, "/v1/admin/users/<email>/toggleAccess")

    # Adds Admin API Endpoints for Analysis Profiles
    api.add_resource(GetAnalysisProfiles, "/v1/admin/analysisProfiles")
    api.add_resource(GetAnalysisProfileById, "/v1/admin/analysisProfiles/<analysis_profile_id>")
    api.add_resource(ApproveAnalysisProfile, "/v1/admin/analysisProfiles/<analysis_profile_id>/approve")
    api.add_resource(ToggelAnalysisProfileStatus, "/v1/admin/analysisProfiles/<analysis_profile_id>/toggleAccess")
    api.add_resource(DeleteAnalysisProfileById, "/v1/admin/analysisProfiles/<analysis_profile_id>")

    # Adds resources for Auth Entity
    api.add_resource(RefreshSession, "/v1/session/refresh")
    api.add_resource(ValidateSession, "/v1/session/validate")

    # Adding api-prefix for logging purposes
    app.config["API_PREFIX"] = api_prefix
