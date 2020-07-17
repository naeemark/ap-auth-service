"""
  User Login Resource
"""
import bcrypt
from flask_restful import reqparse
from flask_restful import Resource
from src.models.user import UserModel
from src.resources.common import create_response_data
from src.utils.constant.response_messages import LOGGED_IN
from src.utils.errors.application_errors import InactiveUserError
from src.utils.errors.application_errors import InvalidCredentialsError
from src.utils.errors.application_errors import PendingApprovalError
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.utils.utils import add_parser_headers_argument
from src.validators.common import check_missing_properties


class LoginUser(Resource):
    """
      Resource LoginUser
    """

    request_parser = reqparse.RequestParser(bundle_errors=True)
    add_parser_headers_argument(parser=request_parser, arg_name="Device-ID")
    add_parser_argument(parser=request_parser, arg_name="email")
    add_parser_argument(parser=request_parser, arg_name="password")

    def post(self):
        """
            Returns a new Token
        """
        try:
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            device_id = data["Device-ID"]
            user = UserModel.get(email=data["email"])

            is_auth_valid = user and bcrypt.checkpw(data["password"].encode(), user.password.encode())
            if not is_auth_valid:
                raise InvalidCredentialsError()
            if not user.is_approved:
                raise PendingApprovalError()
            if not user.is_active:
                raise InactiveUserError()
            response_data = create_response_data(device_id, user.dict())
            return get_success_response(message=LOGGED_IN, data=response_data)

        except Exception as error:
            return get_handled_app_error(error)
