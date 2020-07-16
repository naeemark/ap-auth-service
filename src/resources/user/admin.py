"""
  Admin Endpoints
"""
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.models.user import UserModel as User
from src.utils.application_errors import CallerIsNotAdmin
from src.utils.application_errors import DeactivatedUser
from src.utils.constant.response_messages import ACCOUNT_NOT_ACTIVE
from src.utils.constant.response_messages import GET_ALL_USERS
from src.utils.constant.response_messages import UNAUTHORIZED_REQUEST
from src.utils.errors_collection import inactive_user_401
from src.utils.errors_collection import not_admin_401
from src.utils.response_builder import get_error_response
from src.utils.response_builder import get_success_response


class GetUsers(Resource):
    """ Resource GetUsers """

    @jwt_required
    def get(self):
        """ Get All Users """
        # To-do`s
        # - Check validity of authorization
        # - Check caller is admin
        # - Check caller is active
        # - User Model to get All Users
        # - create response Object and return
        try:
            admin = get_jwt_identity()["user"]

            if not admin["isActive"]:
                raise DeactivatedUser()
            if not admin["isAdmin"]:
                raise CallerIsNotAdmin()

            users = User.get_all()
            users_list = [user.dict() for user in users]

            return get_success_response(message=GET_ALL_USERS, data=users_list)
        except LookupError as error:
            message = str(error).strip("'")
            return get_error_response(status_code=400, message=message)
        except DeactivatedUser:
            return get_error_response(message=ACCOUNT_NOT_ACTIVE, error=inactive_user_401)
        except CallerIsNotAdmin:
            return get_error_response(message=UNAUTHORIZED_REQUEST, error=not_admin_401)
