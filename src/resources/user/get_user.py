"""
  User Login Resource
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.user import UserModel as User
from src.utils.constant.response_messages import GET_USER
from src.utils.errors.application_errors import InvalidJwtCredentialsError
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.response_builder import get_success_response


class GetUser(Resource):
    """
      Resource GetUser
    """

    @jwt_required
    def get(self):
        """
            Returns User object as response based upon the provided Authorization Token
        """
        try:
            jwt_identity = get_jwt_identity()

            if "user" not in jwt_identity or "email" not in jwt_identity["user"]:
                raise InvalidJwtCredentialsError()

            email = jwt_identity["user"]["email"]
            user = User.get(email=email)
            return get_success_response(message=GET_USER, data=user.dict())
        except Exception as error:
            return get_handled_app_error(error)
