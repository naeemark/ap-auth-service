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
from sqlalchemy.exc import OperationalError
from src.models.user import UserModel
from src.utils.blacklist_manager import BlacklistManager
from src.utils.constant.exception import ValidationException
from src.utils.constant.response_messages import LOGOUT
from src.utils.constant.response_messages import UPDATED_PASSWORD
from src.utils.errors import error_handler
from src.utils.errors import ErrorManager as UserError
from src.utils.success_response_manager import get_success_response_login
from src.utils.success_response_manager import get_success_response_register
from src.utils.utils import add_parser_argument
from src.validators.user import ChangePasswordValidate
from src.validators.user import request_body_register
from src.validators.user import UserRegisterValidate
from werkzeug.exceptions import BadRequest


class UserRegister(Resource):
    """
        Resource: User Register
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="email")
    add_parser_argument(parser=request_parser, arg_name="password")

    exception = error_handler.exception_factory()
    server_exception = error_handler.exception_factory("Server")

    @classmethod
    def get_data(cls):
        """gets data from req body"""
        try:
            data = cls.request_parser.parse_args()
        except BadRequest as error:
            return UserRegister.exception.get_response(error_description=str(error))
        return data

    @classmethod
    def apply_validation(cls):
        """validates before processing data"""
        data = cls.get_data()
        email = data["email"]
        req_body_validate = request_body_register(data)

        if req_body_validate:
            return cls.exception.get_response(error_description=req_body_validate)
        try:
            if UserModel.find_by_email(email):
                return cls.exception.get_response(
                    UserError.USER_ALREADY_EXISTS, status=409, response_message=ValidationException.DUPLICATE_USER,
                )
        except OperationalError:
            return cls.server_exception.get_response(UserError.DATABASE_CONNECTION)

        user_register_validate = UserRegisterValidate(data)
        validate_error = user_register_validate.validate_login()

        if validate_error:
            description = validate_error[0]["pre_condition"]
            status_code = validate_error[1]
            title, response_message = (
                (UserError.EMAIL_CONDITION, ValidationException.EMAIL_INCORRECT)
                if status_code == 406
                else (UserError.PASSWORD_PRECONDITION, ValidationException.PASSWORD_CONDITION,)
            )

            return cls.exception.get_response(
                title, status=status_code, error_description=description, response_message=response_message,
            )
        return True

    @classmethod
    def exception_response(cls):
        """checks for possible exceptions """
        data = cls.get_data()
        if isinstance(data, tuple):
            return data
        validate = cls.apply_validation()

        if isinstance(validate, tuple):
            return validate
        return False

    @jwt_required
    def post(self):
        """create user"""
        if UserRegister.exception_response():
            return UserRegister.exception_response()
        data = UserRegister.get_data()
        email = data["email"]
        password = data["password"]
        password = password.encode()
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        try:
            user = UserModel(email, hashed_password)
            user.save_to_db()
        except OperationalError:
            return UserRegister.server_exception.get_response(UserError.DATABASE_CONNECTION)

        current_user = get_jwt_identity()
        return get_success_response_register(identity=current_user)


class UserLogin(Resource):
    """
      Resource UserLogin
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="email")
    add_parser_argument(parser=request_parser, arg_name="password")

    exception = error_handler.exception_factory()
    server_exception = error_handler.exception_factory("Server")

    @classmethod
    def get_data(cls):
        """gets data from req body"""
        try:
            data = cls.request_parser.parse_args()
        except BadRequest as error:
            return UserLogin.exception.get_response(error_description=str(error))
        return data

    @classmethod
    def apply_validation(cls):
        """validates before processing data"""
        data = cls.get_data()
        try:
            user = UserModel.find_by_email(data["email"])
        except OperationalError:
            return cls.server_exception.get_response(UserError.DATABASE_CONNECTION)

        req_body_validate = request_body_register(data)
        if req_body_validate:
            return cls.exception.get_response(error_description=req_body_validate)
        if not user or not bcrypt.checkpw(data["password"].encode(), user.password):
            return cls.exception.get_response(
                UserError.INVALID_CREDENTIAL, status=401, error_description=ValidationException.CREDENTIAL_REQUIRED,
            )
        return True

    @classmethod
    def exception_response(cls):
        """checks for possible exceptions """
        data = cls.get_data()
        if isinstance(data, tuple):
            return data
        validate = cls.apply_validation()
        if isinstance(validate, tuple):
            return validate
        return False

    @jwt_required
    def post(self):
        """
            Returns a new Token
        """
        if UserLogin.exception_response():
            return UserLogin.exception_response()
        data = UserLogin.get_data()
        try:
            user = UserModel.find_by_email(data["email"])
        except OperationalError:
            return UserLogin.server_exception.get_response(UserError.DATABASE_CONNECTION)

        return get_success_response_login(identity=user.id)


class ChangePassword(Resource):
    """
        Resource ChangePassword
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="new_password")

    exception = error_handler.exception_factory()
    server_exception = error_handler.exception_factory("Server")

    @classmethod
    def get_data(cls):
        """gets data from req body"""
        try:
            data = cls.request_parser.parse_args()
        except BadRequest as error:
            return cls.exception.get_response(error_description=str(error))
        return data

    @classmethod
    def apply_validation(cls):
        """validates before processing data"""
        data = cls.get_data()
        req_body_validate = request_body_register(data)
        if req_body_validate:
            return cls.exception.get_response(error_description=req_body_validate)
        data = ChangePassword.request_parser.parse_args()
        change_password_validate = ChangePasswordValidate(data)
        validate = change_password_validate.validate_password()
        status_code = validate[1]
        error_description = validate[0].get("pre_condition")
        if validate[0].get("message"):
            return cls.exception.get_response(
                UserError.PASSWORD_PRECONDITION,
                status=status_code,
                error_description=error_description,
                response_message=ValidationException.PASSWORD_CONDITION,
            )

        return validate[0].get("password_strength")

    @classmethod
    def exception_response(cls):
        """checks for possible exceptions """
        data = cls.get_data()
        if isinstance(data, tuple):
            return data
        validate = cls.apply_validation()

        if isinstance(validate, tuple):
            return validate
        return validate

    @fresh_jwt_required
    def put(self):
        """
            Updates the Model
        """
        current_user = get_jwt_identity()
        validate_pwd = ChangePassword.exception_response()
        data = ChangePassword.get_data()
        try:
            user = UserModel.find_by_id(current_user)
        except OperationalError:
            return ChangePassword.server_exception.get_response(UserError.DATABASE_CONNECTION)
        if not isinstance(validate_pwd, tuple):
            password = data["new_password"].encode()
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            user.password = hashed_password
            user.save_to_db()
            return (
                {
                    "responseMessage": UPDATED_PASSWORD,
                    "responseCode": 200,
                    "response": {"passwordStrength": validate_pwd, "accessToken": None, "refreshToken": None},
                },
                200,
            )
        return validate_pwd


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
        exception = error_handler.exception_factory("Server")
        try:
            BlacklistManager().insert_blacklist_token_id(identity, jti)

            response_logout = {"accessToken": None, "refreshToken": None}

            return (
                {"responseMessage": LOGOUT, "responseCode": 200, "response": response_logout},
                200,
            )
        except ImportError as user_error:
            return exception.get_response(UserError.IMPORT_ERROR, error_description=str(user_error))
        except RedisConnectionUser:
            return exception.get_response(UserError.REDIS_CONNECTION)
