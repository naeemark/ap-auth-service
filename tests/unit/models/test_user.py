"""
    A file to containe all unit tests of
    UserModel
"""
import fakeredis
import pytest
from src.models.user import UserModel
from src.utils.blacklist_manager import BlacklistManager
from src.utils.errors import error_handler as error_test
from src.utils.errors import ErrorManager as ErrorManagerTest


def new_user():
    """
        Creates and return new User
    """
    user = UserModel("abc123@gmail.com", "FlaskIsAwesome")
    return user


def test_new_user():
    """
        Validates newly created User
    """
    # pylint: disable=redefined-outer-name

    assert new_user() is not None
    assert new_user().email == "abc123@gmail.com"
    assert new_user().password == "FlaskIsAwesome"


def test_json_user_model():
    """test json function """

    assert isinstance(new_user().json(), dict)


def test_all_methods_present():
    """test methods """
    list_of_methods = new_user().__dir__()
    assert "save_to_db" in list_of_methods
    assert "find_by_email" in list_of_methods
    assert "find_by_id" in list_of_methods
    assert "delete_from_db" in list_of_methods


def test_blacklist_manager(test_context):
    """fake redis test"""

    token_expire_seconds = test_context[0].config["JWT_ACCESS_TOKEN_EXPIRES"].seconds
    BlacklistManager.initialize_redis(token_expire_seconds, test_context[1])
    blacklist_manager = BlacklistManager()
    blacklist_manager.insert_blacklist_token_id("3", "1231231Xdfwefwe")
    black_list = blacklist_manager.get_jti_list()

    assert isinstance(black_list, list)


def test_jwt_life_span(test_context):
    """life span check"""

    token_expire_seconds = test_context[0].config["JWT_ACCESS_TOKEN_EXPIRES"].seconds
    refresh_token_expire_days = test_context[0].config["JWT_REFRESH_TOKEN_EXPIRES"].days

    assert token_expire_seconds == 1800
    assert refresh_token_expire_days == 7


def test_redis():
    """fake redis test"""
    redis_instance = fakeredis.FakeStrictRedis()
    redis_instance.set("1", "abc")
    redis_instance.set("test", "12")

    assert redis_instance.get("test").decode() == "12"
    assert redis_instance.get("1").decode() == "abc"


class TestErrorFormat:
    """format testing for errors """

    __error_validate_instance = error_test.exception_factory()
    __error_auth_instance = error_test.exception_factory("Auth")
    __error_server_instance = error_test.exception_factory("Server")

    def keys_requirement_satisfied(self, response_dict):
        """checks for keys in response"""
        primary_response_keys = (
            "responseMessage" and "responseCode" and "response" in response_dict.keys()
        )

        if not primary_response_keys:
            return False
        errors_response = response_dict.get("response")["errors"]
        is_list = isinstance(errors_response, list)
        errors_keys_satisfied = (
            "errorCode" and "errorTitle" and "errorDescription" in errors_response[0]
        )
        requirement_clear = is_list and errors_keys_satisfied
        return requirement_clear

    def test_validate_format(self):
        """validation errors format test"""
        validate_response = self.__error_validate_instance.get_response(
            ErrorManagerTest.PASSWORD_PRECONDITION
        )
        keys_check = self.keys_requirement_satisfied(validate_response[0])
        assert isinstance(validate_response, tuple), "error response should be tuple "
        assert isinstance(
            validate_response[1], int
        ), "error response invalid ,it should have status code along it"
        assert keys_check, "error response keys are not satisfied"
        assert validate_response[0]["responseCode"] == 400

    def test_auth_format(self):
        """auth errors format test"""
        validate_response = self.__error_auth_instance.get_response(
            ErrorManagerTest.HEADERS_INCORRECT
        )
        keys_check = self.keys_requirement_satisfied(validate_response[0])
        assert isinstance(validate_response, tuple), "error response should be tuple "
        assert isinstance(
            validate_response[1], int
        ), "error response invalid ,it should have status code along it"
        assert keys_check, "error response keys are not satisfied"
        assert validate_response[0]["responseCode"] == 401

    def test_server_format(self):
        """server errors format test"""
        validate_response = self.__error_server_instance.get_response(
            ErrorManagerTest.REDIS_INSERT
        )
        keys_check = self.keys_requirement_satisfied(validate_response[0])
        assert isinstance(validate_response, tuple), "error response should be tuple "
        assert isinstance(
            validate_response[1], int
        ), "error response invalid ,it should have status code along it"
        assert keys_check, "error response keys are not satisfied"
        assert validate_response[0]["responseCode"] == 500

    @pytest.mark.parametrize(
        "status_code,error_description ,response_message",
        [
            (422, "error description 422", "response msg for 422"),
            (412, "error description 412", "response msg for 412"),
            (406, "error description 406", "response msg for 406"),
        ],
    )
    def test_custom_auth(self, status_code, error_description, response_message):
        """test custom values for auth errors"""

        validate_response = self.__error_auth_instance.get_response(
            ErrorManagerTest.HEADERS_INCORRECT,
            error_description=error_description,
            status=status_code,
            response_message=response_message,
        )
        keys_check = self.keys_requirement_satisfied(validate_response[0])

        assert (
            validate_response[0].get("response")["errors"][0]["errorDescription"]
            == error_description
        )
        assert validate_response[1] == status_code
        assert validate_response[0]["responseMessage"] == response_message
        assert keys_check

    @pytest.mark.parametrize(
        "status_code,error_description ,response_message",
        [
            (400, "error description 400", "response msg for 400"),
            (411, "error description 411", "response msg for 411"),
            (417, "error description 417", "response msg for 417"),
        ],
    )
    def test_custom_validate(self, status_code, error_description, response_message):
        """test custom values for validate errors"""
        validate_response = self.__error_validate_instance.get_response(
            ErrorManagerTest.PASSWORD_PRECONDITION,
            error_description=error_description,
            status=status_code,
            response_message=response_message,
        )
        keys_check = self.keys_requirement_satisfied(validate_response[0])

        assert (
            validate_response[0].get("response")["errors"][0]["errorDescription"]
            == error_description
        )
        assert validate_response[1] == status_code
        assert validate_response[0]["responseMessage"] == response_message
        assert keys_check

    @pytest.mark.parametrize(
        "status_code,error_description ,response_message",
        [
            (500, "error description 500", "response msg for 500"),
            (501, "error description 501", "response msg for 501"),
            (506, "error description 417", "response msg for 506"),
        ],
    )
    def test_custom_server(self, status_code, error_description, response_message):
        """test custom values for server errors"""
        validate_response = self.__error_server_instance.get_response(
            ErrorManagerTest.PASSWORD_PRECONDITION,
            error_description=error_description,
            status=status_code,
            response_message=response_message,
        )
        keys_check = self.keys_requirement_satisfied(validate_response[0])

        assert (
            validate_response[0].get("response")["errors"][0]["errorDescription"]
            == error_description
        )
        assert validate_response[1] == status_code
        assert validate_response[0]["responseMessage"] == response_message
        assert keys_check
