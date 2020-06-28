"""
  auth Resource
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import reqparse
from flask_restful import Resource
from redis.exceptions import ConnectionError as RedisConnectionRefresh
from src.utils.constant.response_messages import REFRESH_SESSION
from src.utils.constant.response_messages import VALIDATE_SESSION
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response
from src.utils.token_manager import blacklist_token
from src.utils.token_manager import get_jwt_tokens
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties


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
                # blacklist Header JWT refresh
                blacklist_token(get_raw_jwt())
                return get_success_response(message=REFRESH_SESSION, data=response_data)
            return get_error_response()
        except RedisConnectionRefresh as error:
            return get_error_response(status_code=503, message=str(error))


class ValidateSession(Resource):
    """
    Validate Session Credentials
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="accessToken")
    add_parser_argument(parser=request_parser, arg_name="refreshToken")

    def post(self):
        """
         Returns access and refresh token
        """
        try:
            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            # To-do`s
            # - verify if tokens are not blacklisted
            # - verify if tokens are not expired
            # - if accessToken is correct:
            #       return success if accessToken is correct
            # - else
            #       create new pair if refreshToken is correct
            #       Discpose old Tokens
            #       Return success Response with new pair of tokens

            # access = verify_token_not_blacklisted(data.accessToken, "access")
            # refresh = verify_token_not_blacklisted(data.refreshToken, "refresh")

            return get_success_response(message=VALIDATE_SESSION, data=data)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
