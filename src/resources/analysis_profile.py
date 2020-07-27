"""
  Analysis Profile Resource
"""
import json
import os
import uuid

import requests
from dynamorm.exceptions import HashKeyExists
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from src.models.analysis_profile import AnalysisProfileModel
from src.utils.errors.application_errors import AnalysisProfileAlreadyExistError
from src.utils.errors.application_errors import ExternalApiInvalidResponseError
from src.utils.errors.application_errors import ResourceNotFoundError
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.logger import log_info
from src.utils.response_builder import get_success_response
from src.utils.utils import add_parser_argument
from src.validators.common import check_missing_properties


class AnalysisProfile(Resource):
    """
        Resource AnalysisProfile
    """

    @jwt_required
    def get(self):
        """ Gets Analysis Profile """
        try:
            user = get_jwt_identity()["user"]
            analysis_profile = AnalysisProfileModel.get(created_by=user["email"])

            if not analysis_profile:
                raise ResourceNotFoundError()
            return get_success_response(message="Get Analysis Profile", data=analysis_profile.dict())
        except Exception as error:
            return get_handled_app_error(error)

    @jwt_required
    def post(self):
        """
            Creates a new Analysis Profile
            Each User is allowed to create only one Analysis Profile
        """
        request_parser = RequestParser()
        add_parser_argument(parser=request_parser, arg_name="zignalProfile", arg_type=dict)
        try:
            user = get_jwt_identity()["user"]

            data = request_parser.parse_args()
            check_missing_properties(data.items())
            zignal_profile_json = data["zignalProfile"]

            # Create Zignal Profile
            result = requests.post(os.environ["ZIGNAL_CREATE_PROFILE_URL"], json=zignal_profile_json)
            result_json = json.loads(result.text)
            log_info(result_json)

            if result.status_code != 200 or "profileId" not in result_json:
                raise ExternalApiInvalidResponseError("From Zignal: {}".format(result_json["error"]))

            analysis_profile_id = str(uuid.uuid4())
            analysis_profile = AnalysisProfileModel(
                created_by=user["email"],
                analysis_profile_id=analysis_profile_id,
                zignal_profile_id=result_json["profileId"],
                zignal_profile_json=zignal_profile_json,
            )
            analysis_profile.save()
            return get_success_response(status_code=201, message="Analysis Profile Created", data={"analysisProfileId": analysis_profile_id})
        except HashKeyExists:
            return get_handled_app_error(AnalysisProfileAlreadyExistError())
        except Exception as error:
            return get_handled_app_error(error)

    @jwt_required
    def put(self):
        """
            Creates a new Analysis Profile
            Each User is allowed to create only one Analysis Profile
        """
        request_parser = RequestParser()
        add_parser_argument(parser=request_parser, arg_name="analysisProfileId")
        add_parser_argument(parser=request_parser, arg_name="zignalProfile", arg_type=dict)
        try:
            user = get_jwt_identity()["user"]
            data = request_parser.parse_args()
            check_missing_properties(data.items())
            zignal_profile_json = data["zignalProfile"]

            analysis_profile = AnalysisProfileModel.get(created_by=user["email"])

            if not analysis_profile or data["analysisProfileId"] != analysis_profile.analysis_profile_id:
                raise ResourceNotFoundError()

            # Delete Zignal Profile
            parts = os.environ["ZIGNAL_CREATE_PROFILE_URL"].split("?")
            put_url = "{}/{}?{}".format(parts[0], analysis_profile.zignal_profile_id, parts[1])
            result = requests.put(put_url, json=zignal_profile_json)
            result_json = json.loads(result.text)
            log_info(result_json)
            if result.status_code != 200:
                raise ExternalApiInvalidResponseError("From Zignal: {}".format(result_json["error"]))

            analysis_profile.update(zignal_profile_json=zignal_profile_json)
            return get_success_response(message="Analysis Profile Updated")
        except Exception as error:
            return get_handled_app_error(error)

    @jwt_required
    def delete(self):
        """ Gets Analysis Profile """
        try:
            user = get_jwt_identity()["user"]
            analysis_profile = AnalysisProfileModel.get(created_by=user["email"])
            if not analysis_profile:
                raise ResourceNotFoundError()

            # Delete Zignal Profile
            parts = os.environ["ZIGNAL_CREATE_PROFILE_URL"].split("?")
            delete_url = "{}/{}?{}".format(parts[0], analysis_profile.zignal_profile_id, parts[1])
            result = requests.delete(delete_url)
            result_json = json.loads(result.text)
            log_info(result_json)
            if result.status_code != 200:
                raise ExternalApiInvalidResponseError("From Zignal: {}".format(result_json["error"]))

            analysis_profile.delete()
            return get_success_response(message="Delete Analysis Profile")
        except Exception as error:
            return get_handled_app_error(error)
