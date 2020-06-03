"""error codes specifications """
from .exception import ValidationException


class ErrorCode:
    """error codes section"""

    INVALID_CREDENTIAL = "Invalid Credential"
    USER_ALREADY_EXISTS = "User Aleardy Exist"
    EMAIL_CONDITION = "Invalid Email"
    PASSWORD_PRECONDITION = "Password Precondition"
    TOKEN_REVOKED = "Token Revoked"
    TOKEN_EXPIRED = "Token Expired"
    TOKEN_INVALID = "Token Invalid"
    HEADERS_INCORRECT = "Invalid Headers"
    REDIS_INSERT = "Redis Server Error"

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
        }
        return (auth.get(error_title), "AUTH_ERROR")

    @classmethod
    def get_server_error(cls, error_title):
        """returns server errors """
        server = {cls.REDIS_INSERT: ValidationException.BLACKLIST}
        return (server.get(error_title), "SERVER_ERROR")

    # 12XX Auth Errors
    AUTH_ERROR = {
        1201: ValidationException.AUTH,
        1202: ValidationException.TOKEN_EXPIRED,
        1203: ValidationException.BLACKLIST,
    }


# success case example
success = {"success": True, "message": "User logged in successfully", "data": {}}

# error case example
fail_case = {
    "success": False,
    "message": "'Password' policy not followed",
    "error_code": 1304,
    "data": {},
}
