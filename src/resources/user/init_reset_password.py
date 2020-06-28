"""
  Init Reset password Resource
"""
from flask_restful import reqparse
from flask_restful import Resource
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties


class InitResetPassword(Resource):
    """
        Resource InitChangePassword
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="email")

    def post(self):
        """
         Send email for reset password
        """
        try:
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            # To-do`s
            # - create a jwtToken to embed in a GET link
            # - trigger ses-email
            return get_success_response(data=data)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
