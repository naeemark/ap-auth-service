"""
  User Logout Resource
"""
from botocore.exceptions import ClientError
from flask_jwt_extended import get_jwt_claims
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.resources.common import blacklist_auth
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import LOGOUT
from src.utils.response_builder import get_error_response
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
        except (ClientError) as error:
            error = DATABASE_CONNECTION if "ResourceNotFoundException" in str(error) else str(error)
            return get_error_response(status_code=503, message=error)
