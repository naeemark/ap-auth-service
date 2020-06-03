"""error codes specifications """
from .exception import ValidationException


class ErrorHandler:
    """error codes section"""

    INVALID_CREDENTIAL = "Invalid Credential"
    USER_ALREADY_EXISTS = "User Aleardy Exist"
    EMAIL_CONDITION = "Invalid Email"
    PASSWORD_PRECONDITION = "Password precondition failed"
    TOKEN_REVOKED = "Token Revoked"
    TOKEN_EXPIRED = "Token Expired"
    TOKEN_INVALID = "Token Invalid"
    HEADERS_INCORRECT = "Invalid Headers"
    REDIS_INSERT = "Redis Server Error"
    FRESH_TOKEN = "Fresh token required"
    IMPORT_ERROR = "Package import error"

    @classmethod
    def get_validation_error(cls, error_title):
        """returns validation errors """
        validation = {
            cls.INVALID_CREDENTIAL: ValidationException.INVALID_CREDENTIAL,
            cls.USER_ALREADY_EXISTS: ValidationException.USER_ALREADY_EXISTS,
            cls.EMAIL_CONDITION: ValidationException.EMAIL_CONDITION,
            cls.PASSWORD_PRECONDITION: ValidationException.PASSWORD_CONDITION,
        }
        return (validation.get(error_title), "VALIDATION_ERROR")

    @classmethod
    def get_auth_error(cls, error_title):
        """returns auth errors """
        auth = {
            cls.TOKEN_REVOKED: ValidationException.TOKEN_REVOKED,
            cls.TOKEN_EXPIRED: ValidationException.TOKEN_EXPIRED,
            cls.TOKEN_INVALID: ValidationException.TOKEN_INVALID,
            cls.HEADERS_INCORRECT: ValidationException.HEADERS_INCORRECT,
            cls.FRESH_TOKEN: ValidationException.FRESH_TOKEN,
        }
        return (auth.get(error_title), "AUTH_ERROR")

    @classmethod
    def get_server_error(cls, error_title):
        """returns server errors """
        server = {
            cls.REDIS_INSERT: ValidationException.BLACKLIST,
            cls.IMPORT_ERROR: ValidationException.IMPORT_ERROR,
        }
        return (server.get(error_title), "SERVER_ERROR")
