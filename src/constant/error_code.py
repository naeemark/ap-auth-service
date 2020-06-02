"""error codes specifications """
from .exception import ValidationException


class ErrorCode:
    """error codes section"""

    # 13XX Session Errors
    SESSION_ERROR = {
        1301: ValidationException.INVALID_CREDENTIAL,
        1302: ValidationException.USER_ALREADY_EXISTS,
        1303: ValidationException.EMAIL_CONDITION,
        1304: ValidationException.PASSWORD_CONDITION,
    }

    # 12XX Auth Errors
    AUTH_ERROR = {
        1201: ValidationException.AUTH,
        1202: ValidationException.TOKEN_EXPIRED,
        1203: ValidationException.BLACKLIST,
    }


# success case example
success = {"success": True, "message": "User logged in successfully", "data": {}}

# error case example
fail_case = {
    "success": False,
    "message": "'Password' policy not followed",
    "error_code": 1304,
    "data": {},
}
