"""
  User Register Resource
"""
import bcrypt
from email_validator import EmailNotValidError
from flask_restful import reqparse
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionUser
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from src.models.user import UserModel
from src.resources.user.common import create_response_data
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import DUPLICATE_USER
from src.utils.constant.response_messages import USER_CREATION
from src.utils.errors_collection import email_not_valid_412
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.utils.utils import add_parser_headers_argument
from src.validators.common import check_missing_properties
from src.validators.user import validate_register_user_data


class RegisterUser(Resource):
    """
        Resource: User Register
    """

    request_parser = reqparse.RequestParser()
    add_parser_headers_argument(parser=request_parser, arg_name="Device-ID")
    add_parser_argument(parser=request_parser, arg_name="name")
    add_parser_argument(parser=request_parser, arg_name="email")
    add_parser_argument(parser=request_parser, arg_name="password")

    # @jwt_required
    def post(self):
        """create new user"""
        try:
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            validate_register_user_data(data=data)

            device_id = data["Device-ID"]
            name, email, password = data["name"], data["email"], data["password"].encode()

            # To-Do need to write the details of the salt
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            # creates and saves a new object
            user = UserModel(email, hashed_password, name)
            user.save_to_db()

            response_data = create_response_data(device_id, user)
            return get_success_response(status_code=201, message=USER_CREATION, data=response_data)
        except IntegrityError:
            return get_error_response(status_code=409, message=DUPLICATE_USER)
        except (OperationalError, RedisConnectionUser) as error:
            error = DATABASE_CONNECTION if isinstance(error, OperationalError) else str(error)
            return get_error_response(status_code=503, message=error)
        except EmailNotValidError as error:
            return get_error_response(status_code=412, message=str(error), error=email_not_valid_412)
        except (LookupError, TypeError) as error:
            return get_error_response(status_code=400, message=str(error))
        except ValueError as error:
            return get_error_response(status_code=412, message=str(error))
