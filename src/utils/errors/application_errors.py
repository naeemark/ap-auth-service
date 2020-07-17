# pylint: disable=missing-class-docstring
"""
    Application Errors
"""
from src.utils.constant.response_messages import ACCOUNT_NOT_ACTIVE
from src.utils.constant.response_messages import ACCOUNT_NOT_APPROVED
from src.utils.constant.response_messages import EMAIL_ALREADY_VERIFIED
from src.utils.constant.response_messages import EMAIL_NOT_FOUND
from src.utils.constant.response_messages import INVALID_CREDENTIAL
from src.utils.constant.response_messages import INVALID_JWT_TOKEN
from src.utils.constant.response_messages import LINK_EXPIRED_ERROR
from src.utils.constant.response_messages import REUSE_PASSWORD_ERROR
from src.utils.constant.response_messages import UNAUTHORIZED_REQUEST
from src.utils.constant.response_messages import USER_ALREADY_APPROVED
from src.utils.constant.response_messages import USER_NOT_FOUND
from src.utils.errors.errors_collection import already_approved_409
from src.utils.errors.errors_collection import email_already_verified_409
from src.utils.errors.errors_collection import inactive_user_401
from src.utils.errors.errors_collection import invalid_credentials_401
from src.utils.errors.errors_collection import invalid_jwt_401
from src.utils.errors.errors_collection import not_admin_401
from src.utils.errors.errors_collection import pending_approval_401
from src.utils.errors.errors_collection import restricted_self_operation_401


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


class UserAlreadyApprovedError(ApplicationError):
    status_code, message, error = 409, USER_ALREADY_APPROVED, already_approved_409


class UserNotFoundError(ApplicationError):
    status_code, message, error = 404, USER_NOT_FOUND, None
