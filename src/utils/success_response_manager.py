"""success response"""
from src.constant.success_message import Success
from src.utils.token_manager import get_token


def response_format(identity, **kwargs):
    """generate common structure of response for success case """
    response_message = kwargs.get("response_message")
    status_code = kwargs.get("status_code") or 200
    fresh_token = kwargs.get("fresh_token") or False
    access_token, refresh_token = get_token(identity=identity, fresh=fresh_token)
    return (
        {
            "responseMessage": response_message,
            "responseCode": status_code,
            "response": {"accessToken": access_token, "refreshToken": refresh_token},
        },
        status_code,
    )


def get_success_response_login(identity):
    """generate login response"""

    return response_format(identity=identity, response_message=Success.LOGGED_IN, fresh_token=True)


def get_success_response_register(identity):
    """generate register response"""

    return response_format(identity=identity, status_code=201, response_message=Success.USER_CREATION)


def get_success_response_session(identity):
    """generate session response"""

    return response_format(identity=identity, response_message=Success.REFRESH_TOKEN)
