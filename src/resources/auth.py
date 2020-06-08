"""
  auth Resource
"""
import base64
import hashlib
import os

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from src.constant.exception import ValidationException
from src.constant.success_message import Success as AuthSuccess
from src.utils.blacklist_manager import BlacklistManager
from src.utils.errors import error_handler
from src.utils.errors import ErrorManager as AuthError
from src.validators.auth import start_session_headers


class StartSession(Resource):
    """
    starts session Resource
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        "Client-App-Token", type=str, location="headers",
    )

    parser.add_argument(
        "Timestamp", type=str, location="headers",
    )

    parser.add_argument(
        "Device-ID", type=str, location="headers",
    )

    @classmethod
    def is_valid_token(cls, client_app_token, timestamp):
        """
            Validates the token and provided parameters
        """
        client_secret_key = os.environ["CLIENT_SECRET_KEY"]
        matcher_string = "{}{}".format(timestamp, client_secret_key)
        hash_string = hashlib.sha256(matcher_string.encode()).digest()
        base64_token = base64.b64encode(hash_string).decode()
        if client_app_token == base64_token:
            return True
        return False

    @classmethod
    def post(cls):
        """
         Returns access and refresh token
        """
        data = cls.parser.parse_args()
        client_app_token = data["Client-App-Token"]
        timestamp = data["Timestamp"]
        device_id = data["Device-ID"]
        headers_validate = start_session_headers(data)
        exception = error_handler.exception_factory()
        validate = cls.is_valid_token(client_app_token, timestamp)
        if headers_validate:
            return exception.get_response(error_description=headers_validate)
        if not validate:
            return exception.get_response(AuthError.HEADERS_INCORRECT)
        access_token = create_access_token(identity=device_id)
        refresh_token = create_refresh_token(identity=device_id)

        return (
            {
                "responseMessage": AuthSuccess.SESSION_START,
                "responseCode": 200,
                "response": {
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
                },
            },
            200,
        )


class TokenRefresh(Resource):
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


class RevokeAccess(Resource):
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
            insert_status = BlacklistManager().insert_blacklist_token_id(identity, jti)
            if not insert_status:
                return exception.get_response(AuthError.REDIS_INSERT)

            return (
                {
                    "responseMessage": AuthSuccess.ACCESS_REVOKED,
                    "responseCode": 200,
                    "response": {"accessToken": None, "refreshToken": None},
                },
                200,
            )
        except ImportError as auth_error:
            ValidationException.IMPORT_ERROR = str(auth_error)
            return exception.get_response(
                AuthError.IMPORT_ERROR, error_description=str(auth_error)
            )
