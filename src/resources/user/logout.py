"""
  User Logout Resource
"""
from datetime import datetime

from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.repositories.black_list import Blacklist
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
        logout the user through jti of token
        """

        try:
            raw_jwt = get_raw_jwt()

            id_access_token = raw_jwt["jti"]
            ttl_access_token = datetime.fromtimestamp(raw_jwt["exp"]).timestamp()

            id_refresh_token = raw_jwt["identity"]["refreshTokenId"]
            ttl_refresh_token = datetime.fromtimestamp(raw_jwt["identity"]["refreshTokenExpire"]).timestamp()

            Blacklist(token_id=id_access_token, type="access", time_to_live=ttl_access_token).save()
            Blacklist(token_id=id_refresh_token, type="refresh", time_to_live=ttl_refresh_token).save()

            return get_success_response(message=LOGOUT)
        except (AttributeError) as error:
            print(error)
            return get_error_response(status_code=503, message=str(error))
