"""
  Init Verify Email Resource
"""
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response


class InitVerifyEmail(Resource):
    """
        Resource InitVerifyEMail
    """

    @jwt_required
    def post(self):
        """
         Send email for verification
        """
        try:
            # To-do`s
            # - Check validity of authorization
            # - extract User's email from JWT token
            # - create a jwtToken to embed in a GET link
            # - trigger ses-email
            return get_success_response()
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
