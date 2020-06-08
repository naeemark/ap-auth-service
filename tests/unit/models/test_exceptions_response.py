"""error handling test"""
import pytest
from src.utils.errors import error_handler as error_test
from src.utils.errors import ErrorManager as ErrorManagerTest


class TestException:
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
            ErrorManagerTest.REDIS_CONNECTION
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
