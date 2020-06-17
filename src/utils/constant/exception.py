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
    BLACKLIST = "Error connecting redis"
    TOKEN_REVOKED = "Token has been revoked"
    TOKEN_INVALID = "Request was well-formed but was unable to be followed due to semantic errors specify correct token"
    HEADERS_INCORRECT = "Bad Headers Provided"
    FRESH_TOKEN = "Login required"
    IMPORT_ERROR = "import error "
    EMAIL_INCORRECT = "Please provide correct email"
    BODY_PROPERTIES_REQUIRED = "Please provide '{properties}'"
    MISSING_AUTH = "Missing Auth"
    CREDENTIAL_REQUIRED = "Invalid email address or password"
    DATABASE = "Error connecting database"
