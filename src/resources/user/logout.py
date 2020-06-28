"""
  User Logout Resource
"""
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionUser
from src.utils.constant.response_messages import LOGOUT
from src.utils.constant.response_messages import REDIS_CONNECTION
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.token_manager import blacklist_token


class LogoutUser(Resource):
    """
    logout user
    """

    @jwt_required
    def post(self):
        """
        logout the user through jti of token ,
         jti is "JWT ID", a unique identifier for a JWT
        """

        try:
            # blacklist Header JWT accessToken
            blacklist_token(get_raw_jwt(), logout=True)
            return get_success_response(message=LOGOUT)
        except (RedisConnectionUser, AttributeError) as error:
            print(error)
            return get_error_response(status_code=503, message=REDIS_CONNECTION)
