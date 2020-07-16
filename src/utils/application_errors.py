"""
    Application Errors
"""


class ApplicationError(Exception):
    """ ApplicationError """


class ErrorDeactivatedUser(ApplicationError):
    """ DeactivatedUser """


class ErrorCallerIsNotAdmin(ApplicationError):
    """ CallerIsNotAdmin """


class ErrorPendingApproval(ApplicationError):
    """ ErrorPendingApproval """


class ErrorUserAlreadyApproved(ApplicationError):
    """ CallerIsNotAdmin """


class ErrorUserNotApprovedYet(ApplicationError):
    """ CallerIsNotAdmin """
