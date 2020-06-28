"""
  Init Verify Email Resource
"""
from flask_jwt_extended import jwt_required
from flask_restful import reqparse as req_parse
from flask_restful import Resource
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument as method_add_parser_argument
from src.validators.common import check_missing_properties as validate_missing_properties


class InitVerifyEmail(Resource):
    """
        Resource InitVerifyEMail
    """

    request_parser = req_parse.RequestParser()
    method_add_parser_argument(parser=request_parser, arg_name="email")

    @jwt_required
    def post(self):
        """
         Returns access and refresh token
        """
        try:
            data = self.request_parser.parse_args()
            validate_missing_properties(data.items())

            # To-do`s
            # - Check validity of authorization
            # - extract User's email from JWT token
            # - create a jwtToken to embed in a GET link
            # - trigger ses-email
            return get_success_response(data=data)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
