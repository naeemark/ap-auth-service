"""
  User Login Resource
"""
import requests
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.utils.errors.application_errors import ExternalApiInvalidResponseError
from src.utils.errors.application_errors import InvalidJwtCredentialsError
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.response_builder import get_success_response

APP_CODE = "590d4706-e3f4-11ea-87d0-0242ac130003"


class Pair2Fa(Resource):
    """
      Pair 2-FA device
    """

    @jwt_required
    def get(self):
        """
            Returns link to the QR code
        """
        try:
            jwt_identity = get_jwt_identity()

            if "user" not in jwt_identity or "email" not in jwt_identity["user"]:
                raise InvalidJwtCredentialsError()

            email = jwt_identity["user"]["email"]

            secret_code = "{}-{}".format(email, APP_CODE)
            pair_url = 'https://www.authenticatorApi.com/pair.aspx?AppName="AleatheaWeb"&AppInfo={}&SecretCode={}'.format(email, secret_code)

            result = requests.get(pair_url)

            if result.status_code != 200:
                raise ExternalApiInvalidResponseError("Error in Pair 2-FA")

            return get_success_response(message="Pair 2-FA", data=result.text)
        except Exception as error:
            return get_handled_app_error(error)


class Validate2Fa(Resource):
    """
      Pair 2-FA device
    """

    @jwt_required
    def get(self, code=None):
        """
            Returns flag is the code is validated or not
        """
        try:
            jwt_identity = get_jwt_identity()

            if "user" not in jwt_identity or "email" not in jwt_identity["user"]:
                raise InvalidJwtCredentialsError()

            email = jwt_identity["user"]["email"]

            secret_code = "{}-{}".format(email, APP_CODE)
            validate_url = "https://www.authenticatorApi.com/Validate.aspx?Pin={}&SecretCode={}".format(code, secret_code)
            result = requests.get(validate_url)
            if result.status_code != 200:
                raise ExternalApiInvalidResponseError("Error in Validate 2-FA")

            flag = bool("true" in result.text.lower())
            return get_success_response(message="Validate 2-FA", data={"validated": flag})
        except Exception as error:
            return get_handled_app_error(error)
