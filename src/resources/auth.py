"""
  auth Resource
"""
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from src.constant.exception import ValidationException
from src.constant.success_message import ACCESS_REVOKED
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
    def post(cls):
        """
         Returns access and refresh token
        """
        data = cls.parser.parse_args()
        client_app_token = data["Client-App-Token"]
        access_token = create_access_token(identity=client_app_token)
        refresh_token = create_refresh_token(client_app_token)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200


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
        return {"access_token": new_token}, 200


class RevokeAccess(Resource):
    """
    logout user
    """

    @jwt_required
    def post(self):
        """
        :return: success message on logout else give error message
        """
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        identity = get_jwt_identity()
        try:
            insert_status = BlacklistManager().insert_blacklist_token_id(identity, jti)
            if not insert_status:
                return {"message": ValidationException.BLACKLIST}, 400
            return {"message": ACCESS_REVOKED}, 200
        except ImportError as error:
            return {"message": error}, 400
        except ValueError as error:
            return {"message": error}, 400