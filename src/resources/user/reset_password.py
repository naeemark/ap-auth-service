"""
  Change / Reset password Resource
"""
import bcrypt
from botocore.exceptions import ClientError
from flask_jwt_extended import decode_token
from flask_restful import reqparse
from flask_restful import Resource
from jwt.exceptions import ExpiredSignatureError
from src.models.black_list import BlacklistModel as Blacklist
from src.models.user import UserModel
from src.resources.common import blacklist_token
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import LINK_EXPIRED_ERROR
from src.utils.constant.response_messages import REUSE_PASSWORD_ERROR
from src.utils.constant.response_messages import UPDATED_PASSWORD
from src.utils.constant.response_messages import USER_NOT_FOUND
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties
from src.validators.user import validate_password_data_param


class ResetPassword(Resource):
    """
        Resource ChangePassword
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="authKey")
    add_parser_argument(parser=request_parser, arg_name="newPassword")

    def post(self):
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
            new_password = data["newPassword"]

            if Blacklist.exists(token_id=token_id):
                raise ExpiredSignatureError()
            validate_password_data_param(password_param=new_password)

            user = UserModel.get(email=email)

            if bcrypt.checkpw(new_password.encode(), user.password.encode()):
                raise ValueError()

            new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            user.update(password=new_hashed_password)
            blacklist_token(token_id=token_id, token_type="access", time_to_live=token_expiry)

            return get_success_response(message=UPDATED_PASSWORD)
        except ClientError as error:
            error = DATABASE_CONNECTION if "ResourceNotFoundException" in str(error) else str(error)
            return get_error_response(status_code=503, message=error)
        except LookupError as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))
        except ExpiredSignatureError:
            return get_error_response(status_code=401, message=LINK_EXPIRED_ERROR)
        except ValueError:
            return get_error_response(status_code=412, message=REUSE_PASSWORD_ERROR)
        except AttributeError:
            return get_error_response(status_code=404, message=USER_NOT_FOUND)
