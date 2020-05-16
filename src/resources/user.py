"""
  User Resource
"""
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import fresh_jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import reqparse
from flask_restful import Resource
from src.constant.exception import ValidationException
from src.constant.success_message import UPDATED_PASSWORD
from src.constant.success_message import USER_CREATION
from src.models.user import UserModel
from src.validation.resources import ChangePasswordValidate
from src.validation.resources import UserRegisterValidate


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help=ValidationException.FIELD_BLANK
    )
    parser.add_argument(
        "password", type=str, required=True, help=ValidationException.FIELD_BLANK
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        email = data["email"]
        password = data["password"]

        if UserModel.find_by_email(email):
            return {"message": ValidationException.USER_ALREDY_EXSIST}, 400

        user_register_validate = UserRegisterValidate(data)
        validate_error = user_register_validate.validate_login()

        if validate_error:
            return validate_error

        password = password.encode()
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        user = UserModel(email, hashed_password)
        user.save_to_db()

        return {"message": USER_CREATION}, 201


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

    @classmethod
    def post(cls):

        data = cls.parser.parse_args()
        user = UserModel.find_by_email(data["email"])

        if user and bcrypt.checkpw(data["password"].encode(), user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": ValidationException.INVALID_CREDENTIAL}, 401


class TokenRefresh(Resource):
    """
        Resource TokenRefresh
    """

    @jwt_refresh_token_required
    def post(self):

        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


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
        else:
            return validate
