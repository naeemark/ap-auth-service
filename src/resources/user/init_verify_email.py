"""
  Init Verify Email Resource
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.user import UserModel as User
from src.resources.common import get_web_auth_jwt_token
from src.utils.application_errors import ErrorEmailAlreadyVerified
from src.utils.constant.response_messages import EMAIL_ALREADY_VERIFIED
from src.utils.constant.response_messages import INVALID_JWT_TOKEN
from src.utils.constant.response_messages import VERIFY_EMAIL_LINK_SENT
from src.utils.email_utils import send_account_verification_email
from src.utils.errors_collection import email_already_verified_409
from src.utils.errors_collection import invalid_credentials_401
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response


class InitVerifyEmail(Resource):
    """
        Resource InitVerifyEMail
    """

    @jwt_required
    def post(self):
        """
         Send email for verification
        """
        try:
            jwt_identity = get_jwt_identity()

            if "user" not in jwt_identity or "email" not in jwt_identity["user"]:
                return get_error_response(status_code=401, message=INVALID_JWT_TOKEN, error=invalid_credentials_401)

            email = jwt_identity["user"]["email"]
            user = User.get(email=email)

            if user.is_email_verified:
                raise ErrorEmailAlreadyVerified()

            jwt_token = get_web_auth_jwt_token({"email": email})
            send_account_verification_email(email=email, auth_key=jwt_token)
            return get_success_response(message=VERIFY_EMAIL_LINK_SENT)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except ErrorEmailAlreadyVerified:
            return get_error_response(status_code=409, message=EMAIL_ALREADY_VERIFIED, error=email_already_verified_409)
