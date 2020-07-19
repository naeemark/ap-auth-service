"""
  Analysis Profile Resource
"""
import uuid

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource
from src.models.analysis_profile import AnalysisProfileModel
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties


class AnalysisProfile(Resource):
    """
        Resource AnalysisProfile
    """

    request_parser = reqparse.RequestParser()
    add_parser_argument(parser=request_parser, arg_name="zignalProfile", arg_type=dict)

    @jwt_required
    def post(self):
        """Returns new Tokens"""
        try:
            user = get_jwt_identity()["user"]

            data = self.request_parser.parse_args()
            check_missing_properties(data.items())

            zignal_profile_json = data["zignalProfile"]

            # To-do - make a check to create a single Zignal Profile for each user

            analysis_profile = AnalysisProfileModel(
                analysis_profile_id=str(uuid.uuid4()), created_by=user["email"], zignal_profile_json=zignal_profile_json
            )
            analysis_profile.save()
            return get_success_response(data=analysis_profile.dict())
        except Exception as error:
            return get_handled_app_error(error)