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
    TOKEN_INVALID = "Invalid token and crypto padding"
    HEADERS_INCORRECT = "Bad Headers Provided"
    FRESH_TOKEN = "Login required"
    IMPORT_ERROR = "import error "
    DUPLICATE_USER = "This email has already been registered"
    EMAIL_INCORRECT = "Provide correct email"
    HEADERS_REQUIRED = "'{properties}' is required"
    BODY_PROPERTIES_REQUIRED = "Provide '{properties}'"
    MISING_AUTH = "Missing Auth"
