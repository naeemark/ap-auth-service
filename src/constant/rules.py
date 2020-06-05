"""
    Password Policy Rules
"""
from password_strength import PasswordPolicy

from .error_handler import ErrorHandler

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
