"""
  User Logout Resource
"""
from flask_jwt_extended import get_jwt_claims
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.resources.common import blacklist_auth
from src.utils.constant.response_messages import LOGOUT
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.response_builder import get_success_response


class LogoutUser(Resource):
    """
    logout user
    """

    @jwt_required
    def post(self):
        """
        logout the user
        """

        try:
            blacklist_auth(get_jwt_claims())
            return get_success_response(message=LOGOUT)
        except Exception as error:
            return get_handled_app_error(error)
