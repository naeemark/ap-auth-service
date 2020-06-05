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
from src.constant.error_handler import ErrorHandler as UserError
from src.constant.exception import ValidationException
from src.constant.success_message import Success
from src.models.user import UserModel
from src.utils.blacklist import BlacklistManager
from src.utils.errors import error_handler
from src.validators.user import ChangePasswordValidate
from src.validators.user import UserRegisterValidate


class UserRegister(Resource):
    """
        Resource: User Register
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
            Creates a new User
        """
        data = UserRegister.parser.parse_args()
        email = data["email"]
        password = data["password"]
        exception = error_handler.exception_factory()

        if UserModel.find_by_email(email):
            return exception.get_response(UserError.USER_ALREADY_EXISTS)

        user_register_validate = UserRegisterValidate(data)
        validate_error = user_register_validate.validate_login()

        if validate_error:
            description = validate_error[0]["pre_condition"]
            status_code = validate_error[1]
            title = (
                UserError.EMAIL_CONDITION
                if status_code == 406
                else UserError.PASSWORD_PRECONDITION
            )

            return exception.get_response(
                title, status=status_code, error_description=description
            )

        password = password.encode()
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        user = UserModel(email, hashed_password)
        user.save_to_db()

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        return (
            {
                "responseMessage": Success.USER_CREATION,
                "responseCode": 201,
                "response": {"token": access_token},
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
                    "responseMessage": Success.LOGGED_IN,
                    "responseCode": 200,
                    "response": {"token": access_token},
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
        "new_password", type=str, required=True, help=ValidationException.FIELD_BLANK
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
                    "responseMessage": Success.UPDATED_PASSWORD,
                    "responseCode": 200,
                    "response": {
                        "passwordStrength": validate[0].get("password_strength")
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
        )


class UserLogout(Resource):
    """
    logout user
    """

    @fresh_jwt_required
    def post(self):
        """
        :return: success message on logout else give error message
        """
        jti = get_raw_jwt()["jti"]
        identity = get_jwt_identity()
        exception = error_handler.exception_factory("Server")
        try:
            insert_status = BlacklistManager().insert_blacklist_token_id(identity, jti)

            if not insert_status:
                return exception.get_response(UserError.REDIS_INSERT)
            return (
                {"responseMessage": Success.LOGOUT, "responseCode": 200},
                200,
            )
        except ImportError as user_error:
            return exception.get_response(
                UserError.IMPORT_ERROR, error_description=str(user_error)
            )
