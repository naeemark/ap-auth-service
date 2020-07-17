# pylint: disable=missing-class-docstring
"""
    Application Errors
"""
from src.utils.constant.response_messages import ACCOUNT_NOT_ACTIVE
from src.utils.constant.response_messages import ACCOUNT_NOT_APPROVED
from src.utils.constant.response_messages import INVALID_CREDENTIAL
from src.utils.errors_collection import inactive_user_401
from src.utils.errors_collection import invalid_credentials_401
from src.utils.errors_collection import pending_approval_401


class ApplicationError(Exception):
    """ ApplicationError """


class InvalidCredentialsError(ApplicationError):
    status_code, message, error = 401, INVALID_CREDENTIAL, invalid_credentials_401


class InactiveUserError(ApplicationError):
    status_code, message, error = 401, ACCOUNT_NOT_ACTIVE, inactive_user_401


class CallerIsNotAdminError(ApplicationError):
    pass


class PendingApprovalError(ApplicationError):
    status_code, message, error = 401, ACCOUNT_NOT_APPROVED, pending_approval_401


class UserAlreadyApprovedError(ApplicationError):
    pass


class UserNotFoundError(ApplicationError):
    pass


class UserNotApprovedYetError(ApplicationError):
    pass


class EmailAlreadyVerifiedError(ApplicationError):
    pass


class CannotPerformSelfOperationError(ApplicationError):
    pass
