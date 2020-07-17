"""
  Change / Reset password Resource
"""
import bcrypt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from src.models.user import UserModel as User
from src.utils.application_errors import InvalidJwtCredentialsError
from src.utils.application_errors import ReusePasswordError
from src.utils.constant.response_messages import UPDATED_PASSWORD
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties
from src.validators.user import validate_password_data_param


class ChangePassword(Resource):
    """
        Resource ChangePassword
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="newPassword")

    @jwt_required
    def put(self):
        """
            Updates the Model
        """
        try:
            payload = get_jwt_identity()
            if "user" not in payload or "email" not in payload["user"]:
                raise InvalidJwtCredentialsError()

            email = payload["user"]["email"]

            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            new_password = data["newPassword"]
            validate_password_data_param(password_param=new_password)
            user = User.get(email=email)

            if bcrypt.checkpw(new_password.encode(), user.password.encode()):
                raise ReusePasswordError()

            new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            user.update(password=new_hashed_password)

            return get_success_response(message=UPDATED_PASSWORD)

        except Exception as error:
            return get_handled_app_error(error)
