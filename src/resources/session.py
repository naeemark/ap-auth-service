"""
  auth Resource
"""
import base64
import hashlib
import os

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionAuth
from src.constant.exception import ValidationException
from src.constant.success_message import Success as AuthSuccess
from src.utils.blacklist_manager import BlacklistManager
from src.utils.errors import error_handler
from src.utils.errors import ErrorManager as AuthError
from src.utils.success_response_manager import get_success_response_session
from src.utils.utils import add_parser_header_argument


class StartSession(Resource):
    """
    starts session Resource
    """

    parser = reqparse.RequestParser()
    add_parser_header_argument(parser=parser, arg_name="Client-App-Token")
    add_parser_header_argument(parser=parser, arg_name="Timestamp", arg_type=int)
    add_parser_header_argument(parser=parser, arg_name="Device-ID")

    @classmethod
    def is_valid_token(cls, client_app_token, timestamp):
        """
            Validates the token and provided parameters
        """
        client_secret_key = os.environ["CLIENT_SECRET_KEY"]
        matcher_string = "{}{}".format(timestamp, client_secret_key)
        hash_string = hashlib.sha256(matcher_string.encode()).digest()
        base64_token = base64.b64encode(hash_string).decode()
        if client_app_token != base64_token:
            raise AttributeError("Bad Headers Provided")

    @classmethod
    def post(cls):
        """
         Returns access and refresh token
        """
        data = cls.parser.parse_args()
        client_app_token = data["Client-App-Token"]
        timestamp = data["Timestamp"]
        device_id = data["Device-ID"]
        exception = error_handler.exception_factory()
        try:
            cls.is_valid_token(client_app_token, timestamp)
            return get_success_response_session(identity=device_id)
        except AttributeError as attribute_error:
            print(attribute_error)
            return exception.get_response(AuthError.HEADERS_INCORRECT)


class RefreshSession(Resource):
    """
        Resource TokenRefresh
    """

    @jwt_refresh_token_required
    def post(self):
        """
            Returns a new Token
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return (
            {
                "responseMessage": AuthSuccess.REFRESH_TOKEN,
                "responseCode": 200,
                "response": {"accessToken": new_token, "refreshToken": None},
            },
            200,
        )


class RevokeSession(Resource):
    """
    logout user
    """

    @jwt_required
    def post(self):
        """
        revoke access for access token
        """
        jti = get_raw_jwt()["jti"]
        identity = get_jwt_identity()
        exception = error_handler.exception_factory("Server")

        try:
            BlacklistManager().insert_blacklist_token_id(identity, jti)

            response_revoke = {"accessToken": None, "refreshToken": None}

            return (
                {"responseMessage": AuthSuccess.ACCESS_REVOKED, "responseCode": 200, "response": response_revoke},
                200,
            )
        except ImportError as auth_error:
            ValidationException.IMPORT_ERROR = str(auth_error)
            return exception.get_response(AuthError.IMPORT_ERROR, error_description=str(auth_error))
        except RedisConnectionAuth:
            return exception.get_response(AuthError.REDIS_CONNECTION)
