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
from src.constant.error_code import ErrorCode
from src.constant.exception import ValidationException
from src.constant.rules import get_error_response as response
from src.constant.success_message import Success
from src.utils.blacklist import BlacklistManager


class StartSession(Resource):
    """
    starts session Resource
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        "Client-App-Token",
        type=str,
        required=True,
        help=ValidationException.FIELD_BLANK,
        location="headers",
    )

    parser.add_argument(
        "Timestamp",
        type=str,
        required=True,
        help=ValidationException.FIELD_BLANK,
        location="headers",
    )

    parser.add_argument(
        "Device-ID",
        type=str,
        required=True,
        help=ValidationException.FIELD_BLANK,
        location="headers",
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
        validate = cls.is_valid_token(client_app_token, timestamp)
        if not validate:
            return (
                {
                    "responseMessage": "Auth error",
                    "responseCode": 400,
                    "response": response(ErrorCode.HEADERS_INCORRECT, "AUTH_ERROR"),
                },
                400,
            )
        access_token = create_access_token(identity=device_id)
        refresh_token = create_refresh_token(identity=device_id)

        return (
            {
                "responseMessage": Success.SESSION_START,
                "responseCode": 200,
                "response": {"token": access_token, "refreshToken": refresh_token},
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
                "responseMessage": Success.REFRESH_TOKEN,
                "responseCode": 200,
                "response": {"token": new_token},
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
        # jti is "JWT ID", a unique identifier for a JWT.
        """
        jti = get_raw_jwt()["jti"]
        identity = get_jwt_identity()
        try:
            insert_status = BlacklistManager().insert_blacklist_token_id(identity, jti)
            if not insert_status:
                return {"message": ValidationException.BLACKLIST}, 400

            return (
                {"responseMessage": Success.ACCESS_REVOKED, "responseCode": 200},
                200,
            )
        except ImportError as error:
            return {"message": error}, 400
        except ValueError as error:
            return {"message": error}, 400
