"""
  User Register Resource
"""
import bcrypt
from flask_restful import reqparse
from flask_restful import Resource
from src.models.user import UserModel
from src.utils.constant.response_messages import SUCCESS_USER_CREATION
from src.utils.errors.error_handler import get_handled_api_error
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties
from src.validators.user import validate_register_user_data


class RegisterUser(Resource):
    """
        Resource: User Register
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="name")
    add_parser_argument(parser=request_parser, arg_name="email")
    add_parser_argument(parser=request_parser, arg_name="password")

    # @jwt_required
    def post(self):
        """create new user"""
        try:
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())
            validate_register_user_data(data=data)

            name, email, password = data["name"], data["email"], data["password"].encode()

            # To-Do need to write the details of the salt
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            # creates and saves a new object
            user = UserModel(email=email, name=name, password=hashed_password)
            user.save()
            return get_success_response(status_code=201, message=SUCCESS_USER_CREATION)

        except Exception as error:
            return get_handled_api_error(error)
