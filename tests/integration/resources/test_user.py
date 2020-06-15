# pylint: disable=unused-argument
"""
    A file to contain all integration tests of
    UserResource
"""
import json

from src.constant.success_message import Success

from ..mock_data import MockDataManager


CONTENT_TYPE_KEY = "Content-Type"
CONTENT_TYPE_VALUE = "application/json"
PASSWORD = "123!!@@AB"


class TestUserBehaviour:
    """
    common user behaviour test cases class
    """

    token_dict = {}
    content_data = {}

    def test_content_data(self, data):
        """content data dest"""
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestUserBehaviour"
        content_data = mock_data_manager.get_content()
        assert isinstance(content_data, dict)
        TestUserBehaviour.content_data.update(content_data)

    def test_register_generated_token(self, test_client, test_database, register_token):
        """
        generete token by register end point
        """
        assert isinstance(register_token, str)
        TestUserBehaviour.token_dict.update({"register_token": register_token})

    def test_login_user(self, api_prefix, test_client):
        """login user for fresh_token and check status in case of login"""
        login_user_data = TestUserBehaviour.content_data["login"]["data"]

        response_login_user = test_client.post(
            f"{api_prefix}/user/login",
            headers={
                "Authorization": f" {TestUserBehaviour.token_dict['register_token']}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps(login_user_data),
            follow_redirects=True,
        )

        fresh_access_token_login = json.loads(response_login_user.data)["response"]["accessToken"]

        assert isinstance(fresh_access_token_login, str)
        assert response_login_user.status_code == 200
        TestUserBehaviour.token_dict.update({"fresh_access_token_login": fresh_access_token_login})

    def test_password_change_without_preconditions(self, api_prefix, test_client):
        """Changing password without preconditons"""
        content_data = TestUserBehaviour.content_data["changePassword_precondition"]["data"]

        fresh_token = TestUserBehaviour.token_dict["fresh_access_token_login"]
        response_password_change = test_client.put(
            f"{api_prefix}/user/changePassword",
            headers={"Authorization": f" {fresh_token}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
            data=json.dumps(content_data),
        )
        assert response_password_change.status_code == 412

    def test_pwd_change_without_fresh_token(self, api_prefix, test_client, session):
        """
        Test case to change password without fresh access token
        """
        content_data = TestUserBehaviour.content_data["changePassword_no_fresh_token"]["data"]

        response_password_change = test_client.put(
            f"{api_prefix}/user/changePassword",
            headers={"Authorization": f" {session[0]}", "Content-Type": "application/json"},
            data=json.dumps(content_data),
        )
        assert response_password_change.status_code == 401

        assert (
            json.loads(response_password_change.data)["response"]["errors"][0]["errorTitle"] == "Fresh token required"
        )

    def test_register_user_without_token(self, api_prefix, test_client):
        """
        Test case to check user register without authentication token
        """
        content_data = TestUserBehaviour.content_data["register_without_token"]["data"]
        response_register_user = test_client.post(f"{api_prefix}/user/register", data=json.dumps(content_data),)
        assert response_register_user.status_code == 401

    def test_register_precondition_password(self, api_prefix, test_client, session):
        """
        Test case to check preconditions applied on password on userregister
        """
        content_data = TestUserBehaviour.content_data["register_precondition_password"]
        register_user = test_client.post(
            content_data["url"].format(prefix=api_prefix),
            headers={"Authorization": f" {session[0]}", "Content-Type": "application/json"},
            data=json.dumps(content_data["data"]),
        )
        assert register_user.status_code == 412

    def test_password_change(self, api_prefix, test_client):
        """password change case """
        content_data = TestUserBehaviour.content_data["password_change"]["data"]

        fresh_token = TestUserBehaviour.token_dict["fresh_access_token_login"]
        response_password_change = test_client.put(
            f"{api_prefix}/user/changePassword",
            headers={"Authorization": f" {fresh_token}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
            data=json.dumps(content_data),
            follow_redirects=True,
        )
        assert response_password_change.status_code == 200

    def test_user_logout(self, api_prefix, test_client):
        """logout user case"""
        fresh_token = TestUserBehaviour.token_dict["fresh_access_token_login"]
        response_logout = test_client.post(
            f"{api_prefix}/user/logout",
            headers={"Authorization": f"{fresh_token}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
        )
        assert response_logout.status_code == 200
        assert json.loads(response_logout.data)["responseMessage"] == Success.LOGOUT
        assert "accessToken" and "refreshToken" in json.loads(response_logout.data)["response"].keys()

    def test_user_logout_without_token(self, api_prefix, test_client):
        """logout user case without token"""
        response_logout = test_client.post(f"{api_prefix}/user/logout", headers={CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE})
        assert response_logout.status_code == 401


class TestSuccessScenario:
    """
    common cases for test by user
    """

    token_dict = {}
    content_data = {}

    def test_content_data(self, data):
        """content data dest"""
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestSuccessScenario"
        content_data = mock_data_manager.get_content()
        assert isinstance(content_data, dict)
        TestSuccessScenario.content_data.update(content_data)

    def test_start_session_success(self, api_prefix, test_client):
        """session start success case"""
        content_data = TestSuccessScenario.content_data["start_session"]["headers"]
        response_start_session = test_client.post(f"{api_prefix}/session/start", headers=content_data,)
        assert "accessToken" and "refreshToken" in json.loads(response_start_session.data)["response"].keys()

    def test_register_user_success(self, api_prefix, test_client, session):
        """register user success case"""
        content_data = TestSuccessScenario.content_data["user_register"]["data"]
        response_register_user = test_client.post(
            f"{api_prefix}/user/register",
            headers={"Authorization": f" {session[0]}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
            data=json.dumps(content_data),
            follow_redirects=True,
        )
        access_token = json.loads(response_register_user.data)["response"]["accessToken"]
        json_data = json.loads(response_register_user.data)
        assert response_register_user.status_code == 201
        assert "accessToken" and "refreshToken" in json_data["response"].keys()
        assert isinstance(json_data["response"]["accessToken"], str)
        assert isinstance(json_data["response"]["refreshToken"], str)
        TestSuccessScenario.token_dict.update({"register_token": access_token})

    def test_login_user_success(self, api_prefix, test_client):
        """valid login case """
        content_data = TestSuccessScenario.content_data["login"]["data"]

        response_login_user = test_client.post(
            f"{api_prefix}/user/login",
            headers={
                "Authorization": f" {TestSuccessScenario.token_dict['register_token']}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps(content_data),
            follow_redirects=True,
        )

        fresh_access_token_login = json.loads(response_login_user.data)["response"]["accessToken"]
        json_data = json.loads(response_login_user.data)
        assert isinstance(fresh_access_token_login, str)
        assert response_login_user.status_code == 200
        assert "accessToken" and "refreshToken" in json_data["response"].keys()
        assert isinstance(json_data["response"]["accessToken"], str)
        assert isinstance(json_data["response"]["refreshToken"], str)


class TestFailureScenario:
    """common failure cases"""

    content_data = {}

    def test_content_data(self, data):
        """content data dest"""
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestFailureScenario"
        content_data = mock_data_manager.get_content()
        assert isinstance(content_data, dict)
        TestFailureScenario.content_data.update(content_data)

    def test_register_email_fail(self, api_prefix, test_client, session):
        """register user failure case"""
        content_data = TestFailureScenario.content_data["user_register_email"]["data"]
        response_register_user = test_client.post(
            f"{api_prefix}/user/register",
            headers={"Authorization": f" {session[0]}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
            data=json.dumps(content_data),
            follow_redirects=True,
        )
        assert response_register_user.status_code == 406

    def test_register_pwd_fail(self, api_prefix, test_client, session):
        """register user failure case"""
        content_data = TestFailureScenario.content_data["user_register_password"]["data"]
        response_register_user = test_client.post(
            f"{api_prefix}/user/register",
            headers={"Authorization": f" {session[0]}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
            data=json.dumps(content_data),
            follow_redirects=True,
        )
        assert response_register_user.status_code == 412
        assert len(json.loads(response_register_user.data)["response"]["errors"]) > 1

    def test_start_session_faliure(self, api_prefix, test_client):
        """session start failure case"""
        content_data = TestFailureScenario.content_data["start_session"]["headers"]
        response_start_session = test_client.post(f"{api_prefix}/session/start", headers=content_data,)

        assert response_start_session.status_code == 400

    def test_register_bad_req(self, api_prefix, test_client, session):
        """register user failure case"""
        content_data = TestFailureScenario.content_data["user_register_bad_req"]["data"]
        response_register_user = test_client.post(
            f"{api_prefix}/user/register",
            headers={"Authorization": f" {session[0]}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
            data=json.dumps(content_data),
            follow_redirects=True,
        )
        assert response_register_user.status_code == 400

    def test_start_session_failure_headers(self, api_prefix, test_client):
        """session start failure case"""
        content_data = TestFailureScenario.content_data["start_session"]["incomplete_headers"]
        response_start_session = test_client.post(f"{api_prefix}/session/start", headers=content_data)
        print(json.loads(response_start_session.data))
        assert response_start_session.status_code == 400
        # assert json.loads(response_start_session.data)["response"]["errors"][0]["errorTitle"] == "Invalid Request"

    def test_missing_jwt(self, api_prefix, test_client):
        """missing auth case"""
        content_data = TestFailureScenario.content_data["user_register_bad_req"]["data"]
        response_register_user = test_client.post(
            f"{api_prefix}/user/register",
            headers={CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
            data=json.dumps(content_data),
            follow_redirects=True,
        )
        assert response_register_user.status_code == 401
        assert json.loads(response_register_user.data)["response"]["errors"][0]["errorTitle"] == "Missing Auth"

    def test_missing_keys_login(self, api_prefix, test_client, session):
        """missing keys in login case"""
        content_data = TestFailureScenario.content_data["login_missing_email"]["data"]
        response_login_user = test_client.post(
            f"{api_prefix}/user/register",
            headers={"Authorization": f" {session[0]}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
            data=json.dumps(content_data),
            follow_redirects=True,
        )
        assert response_login_user.status_code == 400
        assert (
            json.loads(response_login_user.data)["response"]["errors"][0]["errorDescription"]
            == "Please provide 'email'"
        )

    def test_redis_failure(self, api_prefix, test_redis, session):
        """redis failure"""
        response_revoke = test_redis.post(
            f"{api_prefix}/session/revoke",
            headers={"Authorization": f"{session[0]}", CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE},
        )

        assert response_revoke.status_code == 500
        assert json.loads(response_revoke.data)["response"]["errors"][0]["errorDescription"] == "Error connecting redis"
