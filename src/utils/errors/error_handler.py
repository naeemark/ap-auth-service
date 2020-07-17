"""
  Api error Handler
"""
from botocore.exceptions import ClientError
from src.utils.application_errors import InactiveUserError
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.response_builder import get_error_response


def get_handled_api_error(error=None):
    """ Determins the error and return response dict """

    if isinstance(error, InactiveUserError):
        return error.code

    if isinstance(error, ClientError):
        message = DATABASE_CONNECTION if "ResourceNotFoundException" in str(error) else str(error)
        return get_error_response(status_code=503, message=message)

    return get_error_response()
