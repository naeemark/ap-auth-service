"""
  User Resource
"""
import bcrypt
from flask_jwt_extended import fresh_jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionUser
from sqlalchemy.exc import ObjectNotExecutableError
from sqlalchemy.exc import OperationalError
from src.models.user import UserModel
from src.utils.blacklist_manager import BlacklistManager
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import DUPLICATE_USER
from src.utils.constant.response_messages import INVALID_CREDENTIAL
from src.utils.constant.response_messages import LOGOUT
from src.utils.constant.response_messages import REDIS_CONNECTION
from src.utils.constant.response_messages import SESSION_START
from src.utils.constant.response_messages import UPDATED_PASSWORD
from src.utils.constant.response_messages import USER_CREATION
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.token_manager import get_jwt_tokens
from src.utils.utils import add_parser_argument
from src.utils.utils import check_missing_properties
from src.validators.user import UserRegisterValidate


class UserRegister(Resource):
    """
        Resource: User Register
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="email")
    add_parser_argument(parser=request_parser, arg_name="password")

    @classmethod
    def apply_validation(cls):
        """validates before processing data"""
        data = cls.request_parser.parse_args()
        properties_required = check_missing_properties(data.items())
        if properties_required:
            raise KeyError(properties_required)
        email = data["email"]

        try:
            if UserModel.find_by_email(email):
                raise ObjectNotExecutableError(DUPLICATE_USER)
        except OperationalError:
            pass

        user_register_validate = UserRegisterValidate(data)
        validate_error = user_register_validate.validate_login()

        if validate_error:
            description = validate_error[0]["pre_condition"]
            status_code = validate_error[1]

            if status_code == 406:
                raise NameError(description)

            raise ValueError(description)

    @jwt_required
    def post(self):
        """create new user"""
        try:
            self.apply_validation()
            data = self.request_parser.parse_args()
            email, password = data["email"], data["password"]
            password = password.encode()
            # To-Do need to write the details of the salt
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            user = UserModel(email, hashed_password)
            user.save_to_db()
            payload = create_payload(get_jwt_identity(), user)
            print(payload)
            response_data = get_jwt_tokens(payload=payload)
            response_data["user"] = {"email": user.email}
            return get_success_response(status_code=201, message=USER_CREATION, data=response_data)
        except ObjectNotExecutableError:
            return get_error_response(status_code=409, message=DUPLICATE_USER)
        except OperationalError:
            return get_error_response(status_code=503, message=DATABASE_CONNECTION)
        except LookupError as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))
        except NameError as error:
            return get_error_response(status_code=406, message=str(error))
        except ValueError as error:
            return get_error_response(status_code=412, message=str(error))


class UserLogin(Resource):
    """
      Resource UserLogin
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
            data = self.request_parser.parse_args()
            user = UserModel.find_by_email(data["email"])

            if user and bcrypt.checkpw(data["password"].encode(), user.password):
                payload = create_payload(get_jwt_identity(), user)
                response_data = get_jwt_tokens(payload=payload)
                response_data["user"] = {"email": user.email}
                return get_success_response(message=SESSION_START, data=response_data)
            return get_error_response(status_code=401, message=INVALID_CREDENTIAL)
        except OperationalError:
            return get_error_response(status_code=503, message=DATABASE_CONNECTION)


class ChangePassword(Resource):
    """
        Resource ChangePassword
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="new_password")

    @fresh_jwt_required
    def put(self):
        """
            Updates the Model
        """
        payload = get_jwt_identity()
        if "user" not in payload:
            return get_error_response(status_code=401, message=INVALID_CREDENTIAL)
        email = payload["user"]["email"]
        try:
            user = UserModel.find_by_email(email)

            data = self.request_parser.parse_args()
            password = data["new_password"].encode()
            user.password = bcrypt.hashpw(password, bcrypt.gensalt())
            user.save_to_db()
            return get_success_response(message=UPDATED_PASSWORD)
        except OperationalError:
            return get_error_response(status_code=503, message=DATABASE_CONNECTION)


class UserLogout(Resource):
    """
    logout user
    """

    @fresh_jwt_required
    def post(self):
        """
        logout the user through jti of token ,
         jti is "JWT ID", a unique identifier for a JWT
        """
        jti = get_raw_jwt()["jti"]
        identity = get_jwt_identity()
        try:
            BlacklistManager().insert_blacklist_token_id(identity, jti)
            return get_success_response(message=LOGOUT)
        except RedisConnectionUser as redis_service_error:
            print(redis_service_error)
            return get_error_response(status_code=503, message=REDIS_CONNECTION)


def create_payload(jwt_identity, user):
    """Common Method to create payload"""
    payload = {"user": {"email": user.email}}
    if "deviceId" in jwt_identity:
        payload["deviceId"] = jwt_identity["deviceId"]
    return payload
