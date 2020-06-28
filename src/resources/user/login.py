"""
  User Login Resource
"""
import bcrypt
from flask_restful import reqparse
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionUser
from sqlalchemy.exc import OperationalError
from src.models.user import UserModel
from src.resources.user.common import create_response_data
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import INVALID_CREDENTIAL
from src.utils.constant.response_messages import LOGGED_IN
from src.utils.response_builder import get_error_response
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

    # @jwt_required
    def post(self):
        """
            Returns a new Token
        """
        try:
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            device_id = data["Device-ID"]
            user = UserModel.find_by_email(data["email"])

            if user and bcrypt.checkpw(data["password"].encode(), user.password):
                response_data = create_response_data(device_id, user)
                return get_success_response(message=LOGGED_IN, data=response_data)

            return get_error_response(status_code=401, message=INVALID_CREDENTIAL)
        except (OperationalError, RedisConnectionUser) as error:
            error = DATABASE_CONNECTION if isinstance(error, OperationalError) else str(error)
            return get_error_response(status_code=503, message=error)
        except LookupError as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))
