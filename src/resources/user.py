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
from src.constant.success_message import LOGGED_IN
from src.constant.success_message import LOGOUT
from src.constant.success_message import UPDATED_PASSWORD
from src.constant.success_message import USER_CREATION
from src.models.user import UserModel
from src.utils.blacklist import BlacklistManager
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

        if UserModel.find_by_email(email):
            response = {
                "errors": [
                    {
                        "errorCode": "VALIDATION_ERROR",
                        "errorTitle": "We seems to have a problem!",
                        "errorDescription": ValidationException.USER_ALREADY_EXISTS,
                    }
                ]
            }
            return (
                {
                    "responseMessage": "Validation error",
                    "responseCode": 400,
                    "response": response,
                },
                400,
            )

        user_register_validate = UserRegisterValidate(data)
        validate_error = user_register_validate.validate_login()

        if validate_error:
            return validate_error

        password = password.encode()
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        user = UserModel(email, hashed_password)
        user.save_to_db()

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        return (
            {
                "responseMessage": USER_CREATION,
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

        if user and bcrypt.checkpw(data["password"].encode(), user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {"access_token": access_token, "message": LOGGED_IN}, 200
        return {"message": ValidationException.INVALID_CREDENTIAL}, 401


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
        if user and not validate[0].get("message"):
            password = data["new_password"].encode()
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            user.password = hashed_password
            user.save_to_db()
            return (
                {
                    "message": UPDATED_PASSWORD,
                    "password_strength": validate[0].get("password_strength"),
                },
                200,
            )
        return validate


class UserLogout(Resource):
    """
    logout user
    """

    @fresh_jwt_required
    def post(self):
        """
        :return: success message on logout else give error message
        """
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        identity = get_jwt_identity()
        try:
            insert_status = BlacklistManager().insert_blacklist_token_id(identity, jti)

            if not insert_status:
                return {"message": ValidationException.BLACKLIST}, 400
            return {"message": LOGOUT}, 200
        except ImportError as error:
            return {"message": error}, 400
        except ValueError as error:
            return {"message": error}, 400
