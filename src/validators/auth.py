"""validate auth"""
from src.constant.exception import ValidationException

from .common import check_none


def start_session_headers(headers):
    """check if missing header"""
    headers_value_required = tuple(filter(check_none, headers.items()))
    if headers_value_required:
        return ValidationException.HEADERS_REQUIRED.format(
            properties=headers_value_required[0][0]
        )
    return False
