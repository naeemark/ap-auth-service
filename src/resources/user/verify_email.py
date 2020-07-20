"""
  Change / Reset password Resource
"""
from flask_jwt_extended import decode_token
from flask_restful import reqparse
from flask_restful import Resource
from src.models.black_list import BlacklistModel as Blacklist
from src.models.user import UserModel
from src.resources.common import blacklist_token
from src.utils.constant.response_messages import VERIFIED_EMAIL
from src.utils.errors.application_errors import ExpiredEmailedSignatureError
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_query_argument
from src.validators.common import check_missing_properties


class VerifyEmail(Resource):
    """
        Resource VerifyEmail
    """

    request_parser = reqparse.RequestParser()
    add_parser_query_argument(parser=request_parser, arg_name="authKey")

    def get(self):
        """
            Updates the Model
        """

        try:
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            auth_key = data["authKey"]

            decoded_auth = decode_token(auth_key)
            token_id = decoded_auth["user_claims"]["access_token_id"]
            token_expiry = decoded_auth["user_claims"]["expires_access_at"]
            email = decoded_auth["identity"]["email"]

            if Blacklist.exists(token_id=token_id):
                raise ExpiredEmailedSignatureError()

            user = UserModel.get(email=email)
            user.update(is_email_verified=True)
            blacklist_token(token_id=token_id, token_type="access", time_to_live=token_expiry)

            return get_success_response(message=VERIFIED_EMAIL)

        except Exception as error:
            return get_handled_app_error(error)
