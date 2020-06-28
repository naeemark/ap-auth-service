"""
  Change / Reset password Resource
"""
import bcrypt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from sqlalchemy.exc import OperationalError
from src.models.user import UserModel
from src.utils.constant.response_messages import CREDENTIAL_REQUIRED
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import REUSE_PASSWORD_ERROR
from src.utils.constant.response_messages import UPDATED_PASSWORD
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties
from src.validators.user import validate_password_data_param


class ChangePassword(Resource):
    """
        Resource ChangePassword
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="new_password")

    @jwt_required
    def put(self):
        """
            Updates the Model
        """
        payload = get_jwt_identity()
        if "user" not in payload:
            return get_error_response(status_code=400, message=CREDENTIAL_REQUIRED)
        email = payload["user"]["email"]
        try:
            user = UserModel.find_by_email(email)
            data = self.request_parser.parse_args()
            new_password = data["new_password"]

            check_missing_properties(data.items())
            validate_password_data_param(password_param=new_password)

            if bcrypt.checkpw(new_password.encode(), user.password):
                raise ValueError(REUSE_PASSWORD_ERROR)

            user.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            user.save_to_db()

            return get_success_response(message=UPDATED_PASSWORD)
        except OperationalError:
            return get_error_response(status_code=503, message=DATABASE_CONNECTION)
        except LookupError as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))
        except ValueError as error:
            return get_error_response(status_code=412, message=str(error))
