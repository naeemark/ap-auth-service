"""initialized common properties"""
from flask import jsonify


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
    FRESH_TOKEN = "Fresh token required"
    DATABASE_CONNECTION = "Database Server Error"

    @classmethod
    def response(cls, *argv, jsonify_response=False):
        """argv = (error code, error title ,error description, status_code, response message)"""

        error_detail = cls.is_iterative_error(error_code=argv[0], error_title=argv[1], error_description=argv[2])

        response = {
            "responseMessage": argv[4],
            "responseCode": argv[3],
            "response": error_detail,
        }
        if jsonify_response:
            return jsonify(response), argv[3]

        return response, argv[3]

    @classmethod
    def is_iterative_error(cls, **kwargs):
        """multiple errors control"""

        error_code = kwargs.get("error_code")
        error_title = kwargs.get("error_title")
        error_description = kwargs.get("error_description")
        error = {
            "errors": [{"errorCode": error_code, "errorTitle": error_title, "errorDescription": error_description}]
        }
        if isinstance(error_description, list) or isinstance(error_description, tuple):
            errors = [
                {"errorCode": error_code, "errorTitle": error_title, "errorDescription": error_description_index}
                for error_description_index in error_description
            ]
            error.update({"errors": errors})
            return error

        else:

            return error
