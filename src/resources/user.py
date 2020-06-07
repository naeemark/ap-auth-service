"""
  User Resource
"""
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import fresh_jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from src.constant.exception import ValidationException
from src.constant.success_message import Success as UserSuccess
from src.models.user import UserModel
from src.utils.blacklist_manager import BlacklistManager
from src.utils.errors import error_handler
from src.utils.errors import ErrorManager as UserError
from src.validators.user import ChangePasswordValidate
from src.validators.user import request_body_register
from src.validators.user import UserRegisterValidate
from werkzeug.exceptions import BadRequest


class UserRegister(Resource):
    """
        Resource: User Register
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str,
    )
    parser.add_argument(
        "password", type=str,
    )
    exception = error_handler.exception_factory()

    @classmethod
    def get_data(cls):
        """gets data from req body"""
        try:
            data = UserRegister.parser.parse_args()
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
        if UserModel.find_by_email(email):
            return cls.exception.get_response(
                UserError.USER_ALREADY_EXISTS,
                status=409,
                response_message=ValidationException.DUPLICATE_USER,
            )
        user_register_validate = UserRegisterValidate(data)
        validate_error = user_register_validate.validate_login()

        if validate_error:
            description = validate_error[0]["pre_condition"]
            status_code = validate_error[1]
            title, response_message = (
                (UserError.EMAIL_CONDITION, ValidationException.EMAIL_INCORRECT)
                if status_code == 406
                else (
                    UserError.PASSWORD_PRECONDITION,
                    ValidationException.PASSWORD_CONDITION,
                )
            )

            return cls.exception.get_response(
                title,
                status=status_code,
                error_description=description,
                response_message=response_message,
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
        user = UserModel(email, hashed_password)
        user.save_to_db()

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        return (
            {
                "responseMessage": UserSuccess.USER_CREATION,
                "responseCode": 201,
                "response": {"accessToken": access_token, "refreshToken": None},
            },
            201,
        )


class UserLogin(Resource):
    """
      Resource UserLogin
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help=ValidationException.FIELD_BLANK
    )
    parser.add_argument(
        "password", type=str, required=True, help=ValidationException.FIELD_BLANK
    )

    @jwt_required
    def post(self):
        """
            Returns a new Token
        """
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        exception = error_handler.exception_factory()

        if user and bcrypt.checkpw(data["password"].encode(), user.password):
            access_token = create_access_token(identity=user.id, fresh=True)

            return (
                {
                    "responseMessage": UserSuccess.LOGGED_IN,
                    "responseCode": 200,
                    "response": {"accessToken": access_token, "refreshToken": None},
                },
                200,
            )

        return exception.get_response(
            UserError.INVALID_CREDENTIAL,
            status=401,
            error_description="Invalid email address or password",
        )


class ChangePassword(Resource):
    """
        Resource ChangePassword
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        "new_password", type=str,
    )

    @fresh_jwt_required
    def put(self):
        """
            Updates the Model
        """
        current_user = get_jwt_identity()
        data = ChangePassword.parser.parse_args()
        user = UserModel.find_by_id(current_user)
        change_password_validate = ChangePasswordValidate(data)
        validate = change_password_validate.validate_password()

        exception = error_handler.exception_factory()
        if user and not validate[0].get("message"):
            password = data["new_password"].encode()
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            user.password = hashed_password
            user.save_to_db()

            return (
                {
                    "responseMessage": UserSuccess.UPDATED_PASSWORD,
                    "responseCode": 200,
                    "response": {
                        "passwordStrength": validate[0].get("password_strength"),
                        "accessToken": None,
                        "refreshToken": None,
                    },
                },
                200,
            )
        status_code = validate[1]
        error_description = validate[0]["pre_condition"]
        return exception.get_response(
            UserError.PASSWORD_PRECONDITION,
            status=status_code,
            error_description=error_description,
            response_message=ValidationException.PASSWORD_CONDITION,
        )


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
            insert_status = BlacklistManager().insert_blacklist_token_id(identity, jti)

            if not insert_status:
                return exception.get_response(UserError.REDIS_INSERT)
            return (
                {"responseMessage": UserSuccess.LOGOUT, "responseCode": 200},
                200,
            )
        except ImportError as user_error:
            return exception.get_response(
                UserError.IMPORT_ERROR, error_description=str(user_error)
            )
