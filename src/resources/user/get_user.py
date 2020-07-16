"""
  User Login Resource
"""
from botocore.exceptions import ClientError
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.user import UserModel as User
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import GET_USER
from src.utils.constant.response_messages import INVALID_JWT_TOKEN
from src.utils.errors_collection import invalid_credentials_401
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response


class GetUser(Resource):
    """
      Resource GetUser
    """

    @jwt_required
    def get(self):
        """
            Returns User object as response based upon the provided Authorization Token
        """
        try:
            jwt_identity = get_jwt_identity()

            if "user" not in jwt_identity or "email" not in jwt_identity["user"]:
                return get_error_response(status_code=401, message=INVALID_JWT_TOKEN, error=invalid_credentials_401)

            email = jwt_identity["user"]["email"]
            user = User.get(email=email)
            return get_success_response(message=GET_USER, data=user.dict())
        except (ClientError) as error:
            error = DATABASE_CONNECTION if "ResourceNotFoundException" in str(error) else str(error)
            return get_error_response(status_code=503, message=error)
        except LookupError as lookup_error:
            return get_error_response(status_code=400, message=str(lookup_error))
