"""
  Admin Endpoints
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.analysis_profile import AnalysisProfileModel
from src.models.user import UserModel
from src.utils.constant.response_messages import GET_ALL_USERS
from src.utils.constant.response_messages import GET_USER_BY_EMAIL
from src.utils.constant.response_messages import USER_APPROVED
from src.utils.errors.application_errors import CallerIsNotAdminError
from src.utils.errors.application_errors import CannotPerformSelfOperationError
from src.utils.errors.application_errors import InactiveUserError
from src.utils.errors.application_errors import ResourceAlreadyApprovedError
from src.utils.errors.application_errors import ResourceNotFoundError
from src.utils.errors.application_errors import UserAlreadyApprovedError
from src.utils.errors.application_errors import UserNotFoundError
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.logger import log_info
from src.utils.response_builder import get_success_response


class GetUsers(Resource):
    """ Resource GetUsers """

    @jwt_required
    def get(self):
        """ Get All Users """
        try:
            admin = get_jwt_identity()["user"]

            is_authorized(admin=admin)

            users = UserModel.get_all()
            # removes self
            users_list = [user.dict() for user in users if user.email != admin["email"]]
            log_info(f"Users Retrieved: {len(users_list)}")
            return get_success_response(message=GET_ALL_USERS, data=users_list)
        except Exception as error:
            return get_handled_app_error(error)


class GetUserByEmail(Resource):
    """ Resource GetUsers """

    @jwt_required
    def get(self, email=None):
        """ Get All User By Email """
        try:
            admin = get_jwt_identity()["user"]
            is_authorized(admin=admin, target_email=email)

            user = UserModel.get(email=email)
            if not user:
                raise UserNotFoundError()

            return get_success_response(message=GET_USER_BY_EMAIL, data=user.dict())
        except Exception as error:
            return get_handled_app_error(error)


class ApproveUser(Resource):
    """ Resource ApproveUser """

    @jwt_required
    def get(self, email=None):
        """ Approve User """
        try:
            admin = get_jwt_identity()["user"]
            is_authorized(admin=admin, target_email=email)

            user = UserModel.get(email=email)
            if not user:
                raise UserNotFoundError()

            if user.is_approved:
                raise UserAlreadyApprovedError()

            user.update(is_approved=True)
            return get_success_response(message=USER_APPROVED)
        except Exception as error:
            return get_handled_app_error(error)


class ToggelUserAccess(Resource):
    """ Resource ToggelUserAccess """

    @jwt_required
    def get(self, email=None):
        """ Approve User """
        try:
            admin = get_jwt_identity()["user"]
            is_authorized(admin=admin, target_email=email)

            user = UserModel.get(email=email)
            if not user:
                raise UserNotFoundError()
            user.update(is_active=not user.is_active)

            message = "Target User is `{}` now".format("Active" if user.is_active else "Inactive")
            return get_success_response(message=message)
        except Exception as error:
            return get_handled_app_error(error)


class GetAnalysisProfiles(Resource):
    """ Resource GetAnalysisProfiles """

    @jwt_required
    def get(self):
        """ Get All GetAnalysisProfiles """
        try:
            admin = get_jwt_identity()["user"]

            is_authorized(admin=admin)

            analysis_profiles = AnalysisProfileModel.get_all()
            analysis_profiles_list = [analysis_profile.dict() for analysis_profile in analysis_profiles]

            log_info(f"AnalysisProfiles Retrieved: {len(analysis_profiles_list)}")
            return get_success_response(message="Get Analysis Profiles", data=analysis_profiles_list)
        except Exception as error:
            return get_handled_app_error(error)


class GetAnalysisProfileById(Resource):
    """ Resource GetAnalysisProfileById """

    @jwt_required
    def get(self, analysis_profile_id=None):
        """ Get GetAnalysisProfileById """
        try:
            admin = get_jwt_identity()["user"]
            is_authorized(admin=admin)

            analysis_profile = get_analysis_profile(analysis_profile_id=analysis_profile_id)

            return get_success_response(message="Get Analysis Profile by Id", data=analysis_profile.dict())
        except Exception as error:
            return get_handled_app_error(error)


class DeleteAnalysisProfileById(Resource):
    """ Resource GetAnalysisProfileById """

    @jwt_required
    def delete(self, analysis_profile_id=None):
        """ Get GetAnalysisProfileById """
        try:
            admin = get_jwt_identity()["user"]
            is_authorized(admin=admin)

            analysis_profile = get_analysis_profile(analysis_profile_id=analysis_profile_id)
            analysis_profile.delete()

            return get_success_response(message="Analysis Profile Deleted")
        except Exception as error:
            return get_handled_app_error(error)


class ApproveAnalysisProfile(Resource):
    """ Resource ApproveAnalysisProfile """

    @jwt_required
    def get(self, analysis_profile_id=None):
        """ Approve User """
        try:
            admin = get_jwt_identity()["user"]
            is_authorized(admin=admin)

            analysis_profile = get_analysis_profile(analysis_profile_id=analysis_profile_id)

            if analysis_profile.is_approved:
                raise ResourceAlreadyApprovedError()

            analysis_profile.update(is_approved=True)
            return get_success_response(message="Approved Analysis Profile")
        except Exception as error:
            return get_handled_app_error(error)


class ToggelAnalysisProfileStatus(Resource):
    """ Resource ToggelAnalysisProfileStatus """

    @jwt_required
    def get(self, analysis_profile_id=None):
        """ Approve User """
        try:
            admin = get_jwt_identity()["user"]
            is_authorized(admin=admin)

            analysis_profile = get_analysis_profile(analysis_profile_id=analysis_profile_id)

            analysis_profile.update(is_active=not analysis_profile.is_active)
            message = "AnalysisProfile is `{}` now".format("Active" if analysis_profile.is_active else "Inactive")

            return get_success_response(message=message)
        except Exception as error:
            return get_handled_app_error(error)


def is_authorized(admin=None, target_email=None):
    """ Util: validates if the admin is allowed for the actions """

    if not admin["isActive"]:
        raise InactiveUserError()
    if not admin["isAdmin"]:
        raise CallerIsNotAdminError()
    if target_email and admin["email"] == target_email:
        raise CannotPerformSelfOperationError()


# pylint: disable=unnecessary-comprehension
def get_analysis_profile(analysis_profile_id=None):
    """ Util: Gets target AnalysisProfile """
    query_results = AnalysisProfileModel.get_by_id(analysis_profile_id=analysis_profile_id)
    analysis_profiles = [analysis_profile for analysis_profile in query_results]
    if len(analysis_profiles) == 0:
        raise ResourceNotFoundError()
    return analysis_profiles[0]
