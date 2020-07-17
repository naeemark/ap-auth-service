# pylint: disable=missing-class-docstring
"""
    Application Errors
"""


class ApplicationError(Exception):
    """ ApplicationError """


class InactiveUserError(ApplicationError):
    code, message = 400, "Here is message"


class CallerIsNotAdminError(ApplicationError):
    pass


class PendingApprovalError(ApplicationError):
    pass


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
