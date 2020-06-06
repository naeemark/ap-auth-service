"""validate auth"""
from src.constant.exception import ValidationException
from src.constant.headers_properties import header_properties


def check_none(element):
    """filter method"""
    if not element:
        return True
    return False


def start_session_headers(headers):
    """check if missing header"""
    start_session_required = header_properties.get("startSession")
    headers_value_required = tuple(filter(check_none, headers.values()))
    if headers_value_required:
        return ValidationException.HEADERS_REQUIRED.format(
            properties=str(start_session_required)
        )
    return False
