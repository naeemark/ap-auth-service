"""
    Password Policy Rules
"""
from password_strength import PasswordPolicy

from .error_handler import ErrorHandler
from .exception import ValidationException

password_policy = PasswordPolicy.from_names(
    # min length: 8
    length=8,
    # need min. 2 uppercase letters
    uppercase=1,
    # need min. 2 digits
    numbers=2,
    # need min. 2 special characters
    special=1,
    # need min. 2 non-letter characters (digits, specials, anything)
    nonletters=2,
)


def get_error_response(error_title, error_type):
    """response Structure defined"""
    error_instance = {
        "VALIDATION_ERROR": ErrorHandler.get_validation_error(error_title),
        "AUTH_ERROR": ErrorHandler.get_auth_error(error_title),
        "SERVER_ERROR": ErrorHandler.get_server_error(error_title),
    }
    error_description, error_code = error_instance.get(error_type)
    response = {
        "errors": [
            {
                "errorCode": error_code,
                "errorTitle": error_title,
                "errorDescription": error_description,
            }
        ]
    }
    return response


class ErrorManager:
    """manages error"""

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
    def response(cls, *argv):
        """argv = (error code, error title ,error description, status_code, response message)"""
        error_detail = {
            "errors": [
                {
                    "errorCode": argv[0],
                    "errorTitle": argv[1],
                    "errorDescription": argv[2],
                }
            ]
        }

        response = {
            "responseMessage": argv[4],
            "responseCode": argv[3],
            "response": error_detail,
        }
        return response


class AuthError:
    """ it simply returns the auth Error"""

    def __init__(self):
        self.error_response = {
            ErrorManager.TOKEN_REVOKED: ValidationException.TOKEN_REVOKED,
            ErrorManager.TOKEN_EXPIRED: ValidationException.TOKEN_EXPIRED,
            ErrorManager.TOKEN_INVALID: ValidationException.TOKEN_INVALID,
            ErrorManager.HEADERS_INCORRECT: ValidationException.HEADERS_INCORRECT,
            ErrorManager.FRESH_TOKEN: ValidationException.FRESH_TOKEN,
        }
        self.error_code = "AUTH_ERROR"

    def get_response(self, error_title, status_code=401, message="Auth error"):
        """get response for Auth"""
        error_description = self.error_response.get(error_title)

        return ErrorManager.response(
            self.error_code, error_title, error_description, status_code, message
        )


class ValidationError:
    """ it simply returns the Validate Error"""

    def __init__(self):
        self.error_response = {
            ErrorManager.INVALID_CREDENTIAL: ValidationException.INVALID_CREDENTIAL,
            ErrorManager.USER_ALREADY_EXISTS: ValidationException.USER_ALREADY_EXISTS,
            ErrorManager.EMAIL_CONDITION: ValidationException.EMAIL_CONDITION,
            ErrorManager.PASSWORD_PRECONDITION: ValidationException.PASSWORD_CONDITION,
        }
        self.error_code = "VALIDATION_ERROR"

    def get_response(self, error_title, status_code=400, message="Validation error"):
        """get response for validation"""
        error_description = self.error_response.get(error_title)

        return ErrorManager.response(
            self.error_code, error_title, error_description, status_code, message
        )


class ServerError:
    """ it simply returns the Server Error"""

    def __init__(self):
        self.error_response = {
            ErrorManager.REDIS_INSERT: ValidationException.BLACKLIST,
            ErrorManager.IMPORT_ERROR: ValidationException.IMPORT_ERROR,
        }
        self.error_code = "SERVER_ERROR"

    def get_response(self, error_title, status_code=500, message="Server error"):
        """get response for server error"""
        error_description = self.error_response.get(error_title)

        return ErrorManager.response(
            self.error_code, error_title, error_description, status_code, message
        )
