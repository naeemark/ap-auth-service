"""
  auth Resource
"""
from botocore.exceptions import ClientError
from flask_jwt_extended import get_jwt_claims
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.resources.common import blacklist_auth
from src.resources.common import get_jwt_tokens
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import REFRESH_SESSION
from src.utils.constant.response_messages import VALIDATE_SESSION
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response


class RefreshSession(Resource):
    """
        Resource RefreshSession
    """

    @jwt_refresh_token_required
    def post(self):
        """Returns new Tokens"""
        try:
            response_data = get_jwt_tokens(payload=get_jwt_identity())
            blacklist_auth(get_jwt_claims())
            return get_success_response(message=REFRESH_SESSION, data=response_data)
        except (ClientError) as error:
            error = DATABASE_CONNECTION if "ResourceNotFoundException" in str(error) else str(error)
            return get_error_response(status_code=503, message=error)


class ValidateSession(Resource):
    """
    Validate Session Credentials
    """

    @jwt_required
    def get(self):
        """
         Returns success if accessToken is valid
        """
        return get_success_response(message=VALIDATE_SESSION)
