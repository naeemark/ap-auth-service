# pylint: disable=missing-class-docstring
"""
    Application Errors
"""
from src.utils.constant.response_messages import ACCOUNT_NOT_ACTIVE
from src.utils.constant.response_messages import ACCOUNT_NOT_APPROVED
from src.utils.constant.response_messages import DUPLICATE_ANALYSIS_PROFILE
from src.utils.constant.response_messages import DUPLICATE_ENTITY_ERROR
from src.utils.constant.response_messages import DUPLICATE_USER
from src.utils.constant.response_messages import EMAIL_ALREADY_VERIFIED
from src.utils.constant.response_messages import EMAIL_NOT_FOUND
from src.utils.constant.response_messages import EXTERNAL_API_ERROR
from src.utils.constant.response_messages import INVALID_CREDENTIAL
from src.utils.constant.response_messages import INVALID_JWT_TOKEN
from src.utils.constant.response_messages import LINK_EXPIRED_ERROR
from src.utils.constant.response_messages import RESOURCE_ALREADY_APPROVED
from src.utils.constant.response_messages import RESOURCE_NOT_FOUND
from src.utils.constant.response_messages import REUSE_PASSWORD_ERROR
from src.utils.constant.response_messages import UNAUTHORIZED_REQUEST
from src.utils.constant.response_messages import USER_ALREADY_APPROVED
from src.utils.constant.response_messages import USER_NOT_FOUND
from src.utils.errors.errors_collection import already_approved_409
from src.utils.errors.errors_collection import analysis_profile_forbidden_403
from src.utils.errors.errors_collection import email_already_verified_409
from src.utils.errors.errors_collection import entity_conflict_409
from src.utils.errors.errors_collection import external_api_error_400
from src.utils.errors.errors_collection import inactive_user_401
from src.utils.errors.errors_collection import invalid_credentials_401
from src.utils.errors.errors_collection import invalid_jwt_401
from src.utils.errors.errors_collection import not_admin_401
from src.utils.errors.errors_collection import pending_approval_401
from src.utils.errors.errors_collection import resource_already_approved_409
from src.utils.errors.errors_collection import restricted_self_operation_401
from src.utils.errors.errors_collection import user_conflict_409


class ApplicationError(Exception):
    """ ApplicationError """


class CallerIsNotAdminError(ApplicationError):
    status_code, message, error = 401, UNAUTHORIZED_REQUEST, not_admin_401


class CannotPerformSelfOperationError(ApplicationError):
    status_code, message, error = 401, UNAUTHORIZED_REQUEST, restricted_self_operation_401


class EmailAlreadyVerifiedError(ApplicationError):
    status_code, message, error = 409, EMAIL_ALREADY_VERIFIED, email_already_verified_409


class EmailNotRegisteredError(ApplicationError):
    status_code, message, error = 404, EMAIL_NOT_FOUND, None


class ExpiredEmailedSignatureError(ApplicationError):
    status_code, message, error = 401, LINK_EXPIRED_ERROR, None


class InactiveUserError(ApplicationError):
    status_code, message, error = 401, ACCOUNT_NOT_ACTIVE, inactive_user_401


class InvalidCredentialsError(ApplicationError):
    status_code, message, error = 401, INVALID_CREDENTIAL, invalid_credentials_401


class InvalidJwtCredentialsError(ApplicationError):
    status_code, message, error = 401, INVALID_JWT_TOKEN, invalid_jwt_401


class PendingApprovalError(ApplicationError):
    status_code, message, error = 401, ACCOUNT_NOT_APPROVED, pending_approval_401


class ReusePasswordError(ApplicationError):
    status_code, message, error = 412, REUSE_PASSWORD_ERROR, None


class EmailAlreadyExistError(ApplicationError):
    status_code, message, error = 409, DUPLICATE_USER, user_conflict_409


class AnalysisProfileAlreadyExistError(ApplicationError):
    status_code, message, error = 403, DUPLICATE_ANALYSIS_PROFILE, analysis_profile_forbidden_403


class EntityAlreadyExistError(ApplicationError):
    status_code, message, error = 409, DUPLICATE_ENTITY_ERROR, entity_conflict_409


class UserAlreadyApprovedError(ApplicationError):
    status_code, message, error = 409, USER_ALREADY_APPROVED, already_approved_409


class ResourceAlreadyApprovedError(ApplicationError):
    status_code, message, error = 409, RESOURCE_ALREADY_APPROVED, resource_already_approved_409


class UserNotFoundError(ApplicationError):
    status_code, message, error = 404, USER_NOT_FOUND, None


class ResourceNotFoundError(ApplicationError):
    status_code, message, error = 404, RESOURCE_NOT_FOUND, None


class ExternalApiInvalidResponseError(ApplicationError):
    def __init__(self, error=None):  # pylint: disable=super-init-not-called
        self.status_code, self.message, self.error = 400, EXTERNAL_API_ERROR, external_api_error_400
        if error:
            self.error["description"] = error
