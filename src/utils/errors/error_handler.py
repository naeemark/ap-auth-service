# pylint: disable=bad-continuation
"""
  Api error Handler
"""
from botocore.exceptions import ClientError
from dynamorm.exceptions import HashKeyExists
from email_validator import EmailNotValidError
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.errors.application_errors import ApplicationError
from src.utils.errors.application_errors import EntityAlreadyExistError
from src.utils.errors.errors_collection import email_not_valid_412
from src.utils.logger import log_error
from src.utils.response_builder import get_app_error_response
from src.utils.response_builder import get_error_response


def get_handled_app_error(error=None):
    """ Determins the error and return response dict """

    if isinstance(error, (LookupError, TypeError)):
        message = str(error).strip("'")
        return get_error_response(status_code=400, message=message)

    if isinstance(error, ApplicationError):
        return get_app_error_response(error)

    if isinstance(error, HashKeyExists):
        return get_handled_app_error(EntityAlreadyExistError())

    if isinstance(error, ValueError):
        return get_error_response(status_code=412, message=str(error))

    if isinstance(error, EmailNotValidError):
        return get_error_response(status_code=412, message=str(error), error=email_not_valid_412)

    if isinstance(error, ClientError):
        message = DATABASE_CONNECTION if "ResourceNotFoundException" in str(error) else str(error)
        return get_error_response(status_code=503, message=message)

    log_error(str(error))
    return get_error_response()
