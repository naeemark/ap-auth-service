"""
  Admin Endpoints
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.user import UserModel as User
from src.utils.application_errors import CallerIsNotAdminError
from src.utils.application_errors import CannotPerformSelfOperationError
from src.utils.application_errors import InactiveUserError
from src.utils.application_errors import UserAlreadyApprovedError
from src.utils.application_errors import UserNotFoundError
from src.utils.constant.response_messages import GET_ALL_USERS
from src.utils.constant.response_messages import GET_USER_BY_EMAIL
from src.utils.constant.response_messages import TOGGLE_SUCCESS
from src.utils.constant.response_messages import USER_APPROVED
from src.utils.errors.error_handler import get_handled_app_error
from src.utils.logger import info
from src.utils.response_builder import get_success_response


class GetUsers(Resource):
    """ Resource GetUsers """

    @jwt_required
    def get(self):
        """ Get All Users """
        try:
            admin = get_jwt_identity()["user"]

            is_authorized(admin=admin, target_email="admin@alethea.com")

            users = User.get_all()
            # removes self
            users_list = [user.dict() for user in users if user.email != admin["email"]]
            info(f"Users Retrieved: {len(users_list)}")
            return get_success_response(message=GET_ALL_USERS, data=users_list)
        except Exception as error:
            return get_handled_app_error(error)


class GetUserByEmail(Resource):
    """ Resource GetUsers """

    @jwt_required
    def get(self, email=None):
        """ Get All Users """
        try:
            admin = get_jwt_identity()["user"]
            is_authorized(admin=admin, target_email=email)

            user = User.get(email=email)
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

            user = User.get(email=email)
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

            user = User.get(email=email)
            if not user:
                raise UserNotFoundError()
            user.update(is_active=not user.is_active)

            return get_success_response(message=TOGGLE_SUCCESS)
        except Exception as error:
            return get_handled_app_error(error)


def is_authorized(admin=None, target_email=None):
    """ validates if the admin is allowed for the actions """

    if not admin["isActive"]:
        raise InactiveUserError()
    if not admin["isAdmin"]:
        raise CallerIsNotAdminError()
    if target_email and admin["email"] == target_email:
        raise CannotPerformSelfOperationError()
