from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity)
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from constant.exception import Exception
from constant.success_message import USER_CREATION
from validation.resources import UserRegisterValidate


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help=Exception.FEILD_BLANK
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help=Exception.FEILD_BLANK
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        email = data['email']
        password = data['password']

        if UserModel.find_by_email(email):
            return {"message": Exception.USER_ALREDY_EXSIST}, 400

        user_register_validate = UserRegisterValidate(data)
        validate_error = user_register_validate.validate_login()

        if validate_error:
            return validate_error

        user = UserModel(email, password)
        user.save_to_db()

        return {"message": USER_CREATION}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help=Exception.FEILD_BLANK
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help=Exception.FEILD_BLANK
                        )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {"massage": Exception.INVALID_CREDENTIAL}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
