"""
  User Resource
"""
import bcrypt
from email_validator import EmailNotValidError
from flask_jwt_extended import fresh_jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionUser
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from src.models.user import UserModel
from src.utils.constant.response_messages import CREDENTIAL_REQUIRED
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import DUPLICATE_USER
from src.utils.constant.response_messages import INVALID_CREDENTIAL
from src.utils.constant.response_messages import LOGGED_IN
from src.utils.constant.response_messages import LOGOUT
from src.utils.constant.response_messages import REDIS_CONNECTION
from src.utils.constant.response_messages import UPDATED_PASSWORD
from src.utils.constant.response_messages import USER_CREATION
from src.utils.errors_collection import email_not_valid_412
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.token_manager import blacklist_token
from src.utils.token_manager import get_jwt_tokens
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties
from src.validators.user import ChangePasswordValidate
from src.validators.user import validate_register_user_data


class RegisterUser(Resource):
    """
        Resource: User Register
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="email")
    add_parser_argument(parser=request_parser, arg_name="password")

    @jwt_required
    def post(self):
        """create new user"""
        try:
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            validate_register_user_data(None)

            email, password = data["email"], data["password"]
            password = password.encode()
            # To-Do need to write the details of the salt
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            # creates and saves a new object
            user = UserModel(email, hashed_password)
            user.save_to_db()

            payload = create_payload(get_jwt_identity(), user)
            response_data = get_jwt_tokens(payload=payload)
            response_data["user"] = {"email": user.email}

            # blacklist JWT accessToken and refreshToken
            blacklist_token(get_raw_jwt())
            return get_success_response(status_code=201, message=USER_CREATION, data=response_data)
        except IntegrityError:
            return get_error_response(status_code=409, message=DUPLICATE_USER)
        except (OperationalError, RedisConnectionUser) as error:
            error = DATABASE_CONNECTION if isinstance(error, OperationalError) else str(error)
            return get_error_response(status_code=503, message=error)
        except EmailNotValidError as error:
            return get_error_response(status_code=412, message=str(error), error=email_not_valid_412)
        except (LookupError, TypeError) as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))
        except ValueError as error:
            return get_error_response(status_code=412, message=str(error))


class LoginUser(Resource):
    """
      Resource LoginUser
    """

    request_parser = reqparse.RequestParser(bundle_errors=True)
    add_parser_argument(parser=request_parser, arg_name="email")
    add_parser_argument(parser=request_parser, arg_name="password")

    @jwt_required
    def post(self):
        """
            Returns a new Token
        """
        try:
            payload = get_raw_jwt()
            blacklist_token(payload)
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())
            user = UserModel.find_by_email(data["email"])

            if user and bcrypt.checkpw(data["password"].encode(), user.password):
                payload = create_payload(get_jwt_identity(), user)
                response_data = get_jwt_tokens(payload=payload)
                response_data["user"] = {"email": user.email}
                return get_success_response(message=LOGGED_IN, data=response_data)
            return get_error_response(status_code=401, message=INVALID_CREDENTIAL)
        except (OperationalError, RedisConnectionUser) as error:
            error = DATABASE_CONNECTION if isinstance(error, OperationalError) else str(error)
            return get_error_response(status_code=503, message=error)
        except LookupError as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))


class ChangePassword(Resource):
    """
        Resource ChangePassword
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="new_password")
    __password_strength = None

    @classmethod
    def apply_validation(cls):
        """validates before processing data"""
        data = cls.request_parser.parse_args()

        change_password_validate = ChangePasswordValidate(data)
        validate = change_password_validate.validate_password()
        cls.__password_strength = validate[0].get("password_strength")

    @fresh_jwt_required
    def put(self):
        """
            Updates the Model
        """
        payload = get_jwt_identity()
        if "user" not in payload:
            return get_error_response(status_code=400, message=CREDENTIAL_REQUIRED)
        email = payload["user"]["email"]
        try:
            payload = get_raw_jwt()
            blacklist_token(payload)
            user = UserModel.find_by_email(email)
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())
            self.apply_validation()
            password = data["new_password"].encode()
            user.password = bcrypt.hashpw(password, bcrypt.gensalt())
            user.save_to_db()

            return get_success_response(message=UPDATED_PASSWORD, data={"passwordStrength": self.__password_strength})
        except (OperationalError, RedisConnectionUser) as error:
            error = DATABASE_CONNECTION if isinstance(error, OperationalError) else str(error)
            return get_error_response(status_code=503, message=error)
        except LookupError as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))
        except ValueError as error:
            return get_error_response(status_code=412, message=str(error))


class LogoutUser(Resource):
    """
    logout user
    """

    @fresh_jwt_required
    def post(self):
        """
        logout the user through jti of token ,
         jti is "JWT ID", a unique identifier for a JWT
        """

        try:
            payload_data = get_raw_jwt()
            blacklist_token(payload_data, logout=True)
            return get_success_response(message=LOGOUT)
        except (RedisConnectionUser, AttributeError) as error:
            print(error)
            return get_error_response(status_code=503, message=REDIS_CONNECTION)


def create_payload(jwt_identity, user):
    """Common Method to create payload"""
    payload = {"user": {"email": user.email}}
    if "deviceId" in jwt_identity:
        payload["deviceId"] = jwt_identity["deviceId"]
    return payload
