"""error pattern defined"""
from http_status import Status

from . import ErrorManager
from ...constant.exception import ValidationException


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

    def get_response(self, title, status=401, **kwargs):
        """get response for Auth"""
        status_info = Status(status)

        jsonify_response = kwargs.get("jsonify_response")
        description = kwargs.get("error_description")
        response_message = kwargs.get("response_message") or status_info.description

        error_description = (
            description if description else self.error_response.get(title)
        )

        return ErrorManager.response(
            status_info.name.upper(),
            title,
            error_description,
            status,
            response_message,
            jsonify_response=jsonify_response,
        )


class ValidationError:
    """ it simply returns the Validate Error"""

    def __init__(self):
        self.error_response = {
            ErrorManager.INVALID_CREDENTIAL: ValidationException.INVALID_CREDENTIAL,
            ErrorManager.USER_ALREADY_EXISTS: ValidationException.USER_ALREADY_EXISTS,
            ErrorManager.EMAIL_CONDITION: ValidationException.EMAIL_CONDITION,
            ErrorManager.HEADERS_INCORRECT: ValidationException.HEADERS_INCORRECT,
            ErrorManager.PASSWORD_PRECONDITION: ValidationException.PASSWORD_CONDITION,
        }

    def get_response(self, title, status=400, **kwargs):
        """get response for validation"""
        status_info = Status(status)

        jsonify_response = kwargs.get("jsonify_response")
        description = kwargs.get("error_description")
        response_message = kwargs.get("response_message") or status_info.description

        error_description = (
            description if description else self.error_response.get(title)
        )

        return ErrorManager.response(
            status_info.name.upper(),
            title,
            error_description,
            status,
            response_message,
            jsonify_response=jsonify_response,
        )


class ServerError:
    """ it simply returns the Server Error"""

    def __init__(self):
        self.error_response = {
            ErrorManager.REDIS_INSERT: ValidationException.BLACKLIST,
            ErrorManager.IMPORT_ERROR: ValidationException.IMPORT_ERROR,
        }

    def get_response(self, title, status=500, **kwargs):
        """get response for server error"""
        status_info = Status(status)

        jsonify_response = kwargs.get("jsonify_response")
        description = kwargs.get("error_description")
        response_message = kwargs.get("response_message") or status_info.description

        error_description = (
            description if description else self.error_response.get(title)
        )
        return ErrorManager.response(
            status_info.name.upper(),
            title,
            error_description,
            status,
            response_message,
            jsonify_response=jsonify_response,
        )
