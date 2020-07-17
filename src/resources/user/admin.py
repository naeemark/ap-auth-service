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
from src.utils.constant.response_messages import UNAUTHORIZED_REQUEST
from src.utils.constant.response_messages import USER_ALREADY_APPROVED
from src.utils.constant.response_messages import USER_APPROVED
from src.utils.constant.response_messages import USER_NOT_FOUND
from src.utils.errors_collection import already_approved_409
from src.utils.errors_collection import inactive_user_401
from src.utils.errors_collection import not_admin_401
from src.utils.errors_collection import restricted_self_operation_401
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
                raise InactiveUserError()
            if not admin["isAdmin"]:
                raise CallerIsNotAdminError()

            users = User.get_all()
            # removes self
            users_list = [user.dict() for user in users if user.email != admin["email"]]

            return get_success_response(message=GET_ALL_USERS, data=users_list)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except InactiveUserError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=inactive_user_401)
        except CallerIsNotAdminError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=not_admin_401)


class GetUserByEmail(Resource):
    """ Resource GetUsers """

    @jwt_required
    def get(self, email=None):
        """ Get All Users """
        try:
            admin = get_jwt_identity()["user"]

            if not admin["isActive"]:
                raise InactiveUserError()
            if not admin["isAdmin"]:
                raise CallerIsNotAdminError()
            if admin["email"] == email:
                raise CannotPerformSelfOperationError()

            user = User.get(email=email)
            if not user:
                raise UserNotFoundError()

            return get_success_response(message=GET_USER_BY_EMAIL, data=user.dict())
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except InactiveUserError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=inactive_user_401)
        except CallerIsNotAdminError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=not_admin_401)
        except CannotPerformSelfOperationError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=restricted_self_operation_401)
        except UserNotFoundError:
            return get_error_response(status_code=404, message=USER_NOT_FOUND)


class ApproveUser(Resource):
    """ Resource ApproveUser """

    @jwt_required
    def get(self, email=None):
        """ Approve User """
        try:
            admin = get_jwt_identity()["user"]

            if not admin["isActive"]:
                raise InactiveUserError()
            if not admin["isAdmin"]:
                raise CallerIsNotAdminError()
            if admin["email"] == email:
                raise CannotPerformSelfOperationError()

            user = User.get(email=email)
            if not user:
                raise UserNotFoundError()

            if user.is_approved:
                raise UserAlreadyApprovedError()

            user.update(is_approved=True)
            return get_success_response(message=USER_APPROVED)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except InactiveUserError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=inactive_user_401)
        except CallerIsNotAdminError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=not_admin_401)
        except CannotPerformSelfOperationError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=restricted_self_operation_401)
        except UserNotFoundError:
            return get_error_response(status_code=404, message=USER_NOT_FOUND)
        except UserAlreadyApprovedError:
            return get_error_response(status_code=409, message=USER_ALREADY_APPROVED, error=already_approved_409)


class ToggelUserAccess(Resource):
    """ Resource ToggelUserAccess """

    @jwt_required
    def get(self, email=None):
        """ Approve User """
        try:
            admin = get_jwt_identity()["user"]

            if not admin["isActive"]:
                raise InactiveUserError()
            if not admin["isAdmin"]:
                raise CallerIsNotAdminError()
            if admin["email"] == email:
                raise CannotPerformSelfOperationError()

            user = User.get(email=email)
            if not user:
                raise UserNotFoundError()
            user.update(is_active=not user.is_active)

            return get_success_response(message=TOGGLE_SUCCESS)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except InactiveUserError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=inactive_user_401)
        except CallerIsNotAdminError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=not_admin_401)
        except CannotPerformSelfOperationError:
            return get_error_response(status_code=401, message=UNAUTHORIZED_REQUEST, error=restricted_self_operation_401)
        except UserNotFoundError:
            return get_error_response(status_code=404, message=USER_NOT_FOUND)
