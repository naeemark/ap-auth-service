"""success response"""
from src.utils.constant.response_messages import LOGGED_IN
from src.utils.constant.response_messages import USER_CREATION
from src.utils.token_manager import get_jwt_tokens


def response_format(identity, **kwargs):
    """generate common structure of response for success case """
    response_message = kwargs.get("response_message")
    status_code = kwargs.get("status_code") or 200
    tokens = get_jwt_tokens(payload=identity)
    return (
        {"responseMessage": response_message, "responseCode": status_code, "response": tokens},
        status_code,
    )


def get_success_response_login(identity):
    """generate login response"""

    return response_format(identity=identity, response_message=LOGGED_IN, fresh_token=True)


def get_success_response_register(identity):
    """generate register response"""

    return response_format(identity=identity, status_code=201, response_message=USER_CREATION)
