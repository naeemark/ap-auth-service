"""
    Application Errors
"""


class ApplicationError(Exception):
    """ ApplicationError """


class ErrorDeactivatedUser(ApplicationError):
    """ ErrorDeactivatedUser """


class ErrorCallerIsNotAdmin(ApplicationError):
    """ ErrorCallerIsNotAdmin """


class ErrorPendingApproval(ApplicationError):
    """ ErrorPendingApproval """


class ErrorUserAlreadyApproved(ApplicationError):
    """ ErrorUserAlreadyApproved """


class ErrorUserNotFound(ApplicationError):
    """ ErrorUserNotFound """


class ErrorUserNotApprovedYet(ApplicationError):
    """ ErrorUserNotApprovedYet """
