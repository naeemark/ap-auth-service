"""
  Api error Handler
"""
from botocore.exceptions import ClientError
from dynamorm.exceptions import HashKeyExists
from email_validator import EmailNotValidError
from src.utils.application_errors import InactiveUserError
from src.utils.application_errors import InvalidCredentialsError
from src.utils.application_errors import PendingApprovalError
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import DUPLICATE_USER
from src.utils.errors_collection import email_not_valid_412
from src.utils.response_builder import get_app_error_response
from src.utils.response_builder import get_error_response


def get_handled_api_error(error=None):
    """ Determins the error and return response dict """

    if isinstance(error, (LookupError, TypeError)):
        return get_error_response(status_code=400, message=str(error))

    if isinstance(error, (InactiveUserError, InvalidCredentialsError, PendingApprovalError)):
        return get_app_error_response(error)

    if isinstance(error, HashKeyExists):
        return get_error_response(status_code=409, message=DUPLICATE_USER)

    if isinstance(error, ValueError):
        return get_error_response(status_code=412, message=str(error))

    if isinstance(error, EmailNotValidError):
        return get_error_response(status_code=412, message=str(error), error=email_not_valid_412)

    if isinstance(error, InactiveUserError):
        return error.code

    if isinstance(error, ClientError):
        message = DATABASE_CONNECTION if "ResourceNotFoundException" in str(error) else str(error)
        return get_error_response(status_code=503, message=message)

    return get_error_response()
