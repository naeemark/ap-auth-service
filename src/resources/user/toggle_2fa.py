"""
  Change / Reset password Resource
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.user import UserModel
from src.utils.errors.application_errors import InvalidJwtCredentialsError
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.response_builder import get_success_response


class Toggel2Fa(Resource):
    """ Resource Toggel2Fa """

    @jwt_required
    def get(self, email=None):
        """ Toggel2Fa of the User """
        try:
            jwt_identity = get_jwt_identity()

            if "user" not in jwt_identity or "email" not in jwt_identity["user"]:
                raise InvalidJwtCredentialsError()

            email = jwt_identity["user"]["email"]
            user = UserModel.get(email=email)
            user.update(is_2fa_enabled=not user.is_2fa_enabled)

            message = "Your 2-FA is `{}` now".format("Enabled" if user.is_2fa_enabled else "Disabled")
            return get_success_response(message=message)
        except Exception as error:
            return get_handled_app_error(error)
