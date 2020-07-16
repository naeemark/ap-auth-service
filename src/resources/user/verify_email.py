"""
  Change / Reset password Resource
"""
from botocore.exceptions import ClientError
from flask_jwt_extended import decode_token
from flask_restful import reqparse
from flask_restful import Resource
from jwt.exceptions import ExpiredSignatureError
from src.models.black_list import BlacklistModel as Blacklist
from src.models.user import UserModel as User
from src.resources.common import blacklist_token
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import LINK_EXPIRED_ERROR
from src.utils.constant.response_messages import VERIFIED_EMAIL
from src.utils.response_builder import get_error_response
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
                raise ExpiredSignatureError()

            user = User.get(email=email)
            user.update(is_email_verified=True)
            blacklist_token(token_id=token_id, token_type="access", time_to_live=token_expiry)

            return get_success_response(message=VERIFIED_EMAIL)
        except ClientError as error:
            error = DATABASE_CONNECTION if "ResourceNotFoundException" in str(error) else str(error)
            return get_error_response(status_code=503, message=error)
        except LookupError as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))
        except ExpiredSignatureError:
            return get_error_response(status_code=401, message=LINK_EXPIRED_ERROR)
