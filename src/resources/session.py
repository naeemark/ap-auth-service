"""
  auth Resource
"""
import base64
import hashlib
import os

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionAuth
from src.utils import response_builder
from src.utils.blacklist_manager import BlacklistManager
from src.utils.constant.response_messages import ACCESS_REVOKED
from src.utils.constant.response_messages import HEADERS_INCORRECT
from src.utils.constant.response_messages import REDIS_CONNECTION
from src.utils.constant.response_messages import REFRESH_TOKEN
from src.utils.constant.response_messages import SESSION_START
from src.utils.token_manager import get_jwt_tokens
from src.utils.utils import add_parser_headers_argument
from src.utils.utils import check_missing_properties


class StartSession(Resource):
    """
    starts session Resource
    """

    parser = reqparse.RequestParser(bundle_errors=True)
    add_parser_headers_argument(parser=parser, arg_name="Client-App-Token")
    add_parser_headers_argument(parser=parser, arg_name="Timestamp", arg_type=int)
    add_parser_headers_argument(parser=parser, arg_name="Device-ID")

    @classmethod
    def is_valid_token(cls, client_app_token, timestamp):
        """
            Validates the token and provided parameters
        """
        properties_required = check_missing_properties(cls.parser.parse_args().items())
        if properties_required:
            raise KeyError(properties_required)
        client_secret_key = os.environ["CLIENT_SECRET_KEY"]
        matcher_string = "{}{}".format(timestamp, client_secret_key)
        hash_string = hashlib.sha256(matcher_string.encode()).digest()
        base64_token = base64.b64encode(hash_string).decode()
        if client_app_token != base64_token:
            raise AttributeError(HEADERS_INCORRECT)

    @classmethod
    def post(cls):
        """
         Returns access and refresh token
        """
        data = cls.parser.parse_args()
        client_app_token = data["Client-App-Token"]
        timestamp = data["Timestamp"]
        device_id = data["Device-ID"]
        try:
            cls.is_valid_token(client_app_token, timestamp)
            response_data = get_jwt_tokens(payload={"deviceId": device_id})
            return response_builder.get_success_response(message=SESSION_START, data=response_data)
        except AttributeError as attribute_error:
            # TO-DO: need to log the error
            return response_builder.get_error_response(status_code=400, message=str(attribute_error))
        except LookupError as lookup_error:
            return response_builder.get_error_response(status_code=400, message=str(lookup_error))


class RefreshSession(Resource):
    """
        Resource RefreshSession
    """

    @jwt_refresh_token_required
    def post(self):
        """Returns new Tokens"""
        payload = get_jwt_identity()
        # TO-DO: need to log the payload
        response_data = get_jwt_tokens(payload=payload)
        if response_data:
            return response_builder.get_success_response(message=REFRESH_TOKEN, data=response_data)
        return response_builder.get_error_response()


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
        payload = get_jwt_identity()
        try:
            BlacklistManager().insert_blacklist_token_id(payload, jti)
            return response_builder.get_success_response(message=ACCESS_REVOKED)
        # TO-DO: seriously required some change here ref: ImportError
        except ImportError as auth_error:
            return response_builder.get_error_response(message=str(auth_error))
        except RedisConnectionAuth:
            return response_builder.get_error_response(message=REDIS_CONNECTION)
