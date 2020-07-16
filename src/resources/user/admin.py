"""
  Admin Endpoints
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.user import UserModel as User
from src.utils.application_errors import ErrorCallerIsNotAdmin
from src.utils.application_errors import ErrorDeactivatedUser
from src.utils.application_errors import ErrorUserAlreadyApproved
from src.utils.constant.response_messages import ACCOUNT_NOT_ACTIVE
from src.utils.constant.response_messages import GET_ALL_USERS
from src.utils.constant.response_messages import UNAUTHORIZED_REQUEST
from src.utils.constant.response_messages import USER_ALREADY_APPROVED
from src.utils.constant.response_messages import USER_APPROVED
from src.utils.errors_collection import already_approved_409
from src.utils.errors_collection import inactive_user_401
from src.utils.errors_collection import not_admin_401
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response


class GetUsers(Resource):
    """ Resource GetUsers """

    @jwt_required
    def get(self):
        """ Get All Users """
        try:
            admin = get_jwt_identity()["user"]

            if not admin["isActive"]:
                raise ErrorDeactivatedUser()
            if not admin["isAdmin"]:
                raise ErrorCallerIsNotAdmin()

            users = User.get_all()
            users_list = [user.dict() for user in users]

            return get_success_response(message=GET_ALL_USERS, data=users_list)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except ErrorDeactivatedUser:
            return get_error_response(status_code=401, message=ACCOUNT_NOT_ACTIVE, error=inactive_user_401)
        except ErrorCallerIsNotAdmin:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=not_admin_401)


class ApproveUser(Resource):
    """ Resource GetUsers """

    @jwt_required
    def get(self, email=None):
        """ Approve User """
        try:
            admin = get_jwt_identity()["user"]

            if not admin["isActive"]:
                raise ErrorDeactivatedUser()
            if not admin["isAdmin"]:
                raise ErrorCallerIsNotAdmin()

            user = User.get(email=email)
            if user.is_approved:
                raise ErrorUserAlreadyApproved()

            user.update(is_approved=True)
            return get_success_response(message=USER_APPROVED)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except ErrorDeactivatedUser:
            return get_error_response(status_code=401, message=ACCOUNT_NOT_ACTIVE, error=inactive_user_401)
        except ErrorCallerIsNotAdmin:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=not_admin_401)
        except ErrorUserAlreadyApproved:
            return get_error_response(status_code=409, message=USER_ALREADY_APPROVED, error=already_approved_409)
