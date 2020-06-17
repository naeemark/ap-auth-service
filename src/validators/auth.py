"""validate auth"""
from src.utils.constant.response_messages import HEADERS_REQUIRED
from src.utils.utils import check_none


def start_session_headers(headers):
    """check if missing header"""
    headers_value_required = tuple(filter(check_none, headers.items()))
    if headers_value_required:
        return HEADERS_REQUIRED.format(properties=headers_value_required[0][0])
    return False
