"""
  auth Resource
"""
import base64
import hashlib
import os

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import reqparse
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionRefresh
from src.utils.constant.response_messages import HEADERS_INCORRECT
from src.utils.constant.response_messages import REDIS_CONNECTION
from src.utils.constant.response_messages import REFRESH_TOKEN
from src.utils.constant.response_messages import REFRESH_TOKEN_REVOKED
from src.utils.constant.response_messages import SESSION_START
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.token_manager import get_jwt_tokens
from src.utils.utils import add_parser_headers_argument
from src.utils.utils import blacklist_token
from src.validators.common import check_missing_properties


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
        client_secret_key = os.environ["CLIENT_SECRET_KEY"]
        matcher_string = "{}{}".format(timestamp, client_secret_key)
        hash_string = hashlib.sha256(matcher_string.encode()).digest()
        base64_token = base64.b64encode(hash_string).decode()
        if client_app_token != base64_token:
            raise AttributeError()

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
            check_missing_properties(data.items())
            cls.is_valid_token(client_app_token, timestamp)
            response_data = get_jwt_tokens(payload={"deviceId": device_id})
            return get_success_response(message=SESSION_START, data=response_data)
        except AttributeError as attribute_error:
            # TO-DO: need to log the error
            print(attribute_error)
            return get_error_response(status_code=400, message=HEADERS_INCORRECT)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)


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
        try:
            if response_data:
                payload_data = get_raw_jwt()
                blacklist_token(payload_data)
                return get_success_response(message=REFRESH_TOKEN, data=response_data)
            return get_error_response()
        except RedisConnectionRefresh as error:
            return get_error_response(status_code=503, message=str(error))


class RevokeRefreshSession(Resource):
    """
    revoke refresh token
    """

    @jwt_refresh_token_required
    def post(self):
        """
        revoke access for refresh token
        """

        try:
            payload_data = get_raw_jwt()
            blacklist_token(payload_data)
            return get_success_response(message=REFRESH_TOKEN_REVOKED)
        except RedisConnectionRefresh:
            return get_error_response(status_code=503, message=REDIS_CONNECTION)
