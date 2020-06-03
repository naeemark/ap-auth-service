"""
Exceptions
"""


class ValidationException(Exception):
    """A Custom Validation Exception"""

    USER_ALREADY_EXISTS = "A user with that email already exists"
    FIELD_BLANK = "This field cannot be blank"
    INVALID_CREDENTIAL = "Invalid credentials"
    PASSWORD_CONDITION = "'Password' policy not followed"
    EMAIL_CONDITION = "'email' is not valid"
    AUTH = "Authorization Required"
    TOKEN_EXPIRED = "Token has expired"
    BLACKLIST = "Error occurred inserting token"
    TOKEN_REVOKED = "Token has been revoked"
