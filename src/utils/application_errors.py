# pylint: disable=missing-class-docstring
"""
    Application Errors
"""
from src.utils.constant.response_messages import ACCOUNT_NOT_ACTIVE
from src.utils.constant.response_messages import ACCOUNT_NOT_APPROVED
from src.utils.constant.response_messages import EMAIL_ALREADY_VERIFIED
from src.utils.constant.response_messages import INVALID_CREDENTIAL
from src.utils.constant.response_messages import INVALID_JWT_TOKEN
from src.utils.constant.response_messages import REUSE_PASSWORD_ERROR
from src.utils.errors_collection import email_already_verified_409
from src.utils.errors_collection import inactive_user_401
from src.utils.errors_collection import invalid_credentials_401
from src.utils.errors_collection import invalid_jwt_401
from src.utils.errors_collection import pending_approval_401


class ApplicationError(Exception):
    """ ApplicationError """


class InvalidCredentialsError(ApplicationError):
    status_code, message, error = 401, INVALID_CREDENTIAL, invalid_credentials_401


class InvalidJwtCredentialsError(ApplicationError):
    status_code, message, error = 401, INVALID_JWT_TOKEN, invalid_jwt_401


class InactiveUserError(ApplicationError):
    status_code, message, error = 401, ACCOUNT_NOT_ACTIVE, inactive_user_401


class CallerIsNotAdminError(ApplicationError):
    pass


class PendingApprovalError(ApplicationError):
    status_code, message, error = 401, ACCOUNT_NOT_APPROVED, pending_approval_401


class ReusePasswordError(ApplicationError):
    status_code, message, error = 412, REUSE_PASSWORD_ERROR, None


class UserAlreadyApprovedError(ApplicationError):
    pass


class UserNotFoundError(ApplicationError):
    pass


class UserNotApprovedYetError(ApplicationError):
    pass


class EmailAlreadyVerifiedError(ApplicationError):
    status_code, message, error = 409, EMAIL_ALREADY_VERIFIED, email_already_verified_409


class CannotPerformSelfOperationError(ApplicationError):
    pass
