"""
  Init Verify Email Resource
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.user import UserModel as User
from src.resources.common import get_web_auth_jwt_token
from src.utils.constant.response_messages import VERIFY_EMAIL_LINK_SENT
from src.utils.email_utils import send_account_verification_email
from src.utils.errors.application_errors import EmailAlreadyVerifiedError
from src.utils.errors.application_errors import InvalidJwtCredentialsError
from src.utils.errors.error_handler import get_handled_app_error
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
                raise InvalidJwtCredentialsError()

            email = jwt_identity["user"]["email"]
            user = User.get(email=email)

            if user.is_email_verified:
                raise EmailAlreadyVerifiedError()

            jwt_token = get_web_auth_jwt_token({"email": email})
            send_account_verification_email(email=email, auth_key=jwt_token)
            return get_success_response(message=VERIFY_EMAIL_LINK_SENT)
        except Exception as error:
            return get_handled_app_error(error)
