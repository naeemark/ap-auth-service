"""initialized common properties"""


class ErrorManager:
    """manages error"""

    INVALID_CREDENTIAL = "Invalid Credential"
    USER_ALREADY_EXISTS = "User Aleardy Exist"
    EMAIL_CONDITION = "Invalid Email"
    PASSWORD_PRECONDITION = "Password precondition failed"
    TOKEN_REVOKED = "Token Revoked"
    TOKEN_EXPIRED = "Token Expired"
    TOKEN_INVALID = "Token Invalid"
    HEADERS_INCORRECT = "Invalid Headers"
    REDIS_INSERT = "Redis Server Error"
    FRESH_TOKEN = "Fresh token required"
    IMPORT_ERROR = "Package import error"

    @classmethod
    def response(cls, *argv):
        """argv = (error code, error title ,error description, status_code, response message)"""
        error_detail = {
            "errors": [
                {
                    "errorCode": argv[0],
                    "errorTitle": argv[1],
                    "errorDescription": argv[2],
                }
            ]
        }

        response = {
            "responseMessage": argv[4],
            "responseCode": argv[3],
            "response": error_detail,
        }
        return response
