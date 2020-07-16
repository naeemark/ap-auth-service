"""
    Application Errors
"""


class ApplicationError(Exception):
    """ ApplicationError """


class DeactivatedUser(ApplicationError):
    """ DeactivatedUser """


class CallerIsNotAdmin(ApplicationError):
    """ CallerIsNotAdmin """
