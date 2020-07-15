"""
  Init Reset password Resource
"""
from flask_restful import reqparse
from flask_restful import Resource
from src.models.user import UserModel
from src.resources.common import get_web_auth_jwt_token
from src.utils.constant.response_messages import RESET_PASSWORD_LINK_SENT
from src.utils.constant.response_messages import USER_NOT_FOUND
from src.utils.email_utils import send_reset_password_email
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

            email = data["email"]
            user = UserModel.get(email=email)
            if not user:
                raise AttributeError()

            jwt_token = get_web_auth_jwt_token({"email": email})
            send_reset_password_email(email=email, auth_key=jwt_token)

            return get_success_response(message=RESET_PASSWORD_LINK_SENT)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except AttributeError:
            return get_error_response(status_code=404, message=USER_NOT_FOUND)
