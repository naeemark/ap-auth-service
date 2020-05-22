# pylint: disable=unused-argument
"""
    A file to containe all integration tests of
    UserResource
"""
import json


def test_sum(test_client, test_database):
    """
        A sample test to demostrate the availability of test_client and test_dataabase
    """
    # for mock purpose
    assert 1 + 1 == 2


CONTENT_TYPE_KEY = "Content-Type"
CONTENT_TYPE_VALUE = "application/json"
PASSWORD = "123!!@@AB"


class TestUserBehaviour:
    """
    common user behaviour test cases class
    """

    token_dict = {}

    def test_register_generated_token(self, register_token):
        """
        generete token by register end point
        """
        assert isinstance(register_token, str)
        TestUserBehaviour.token_dict.update({"register_token": register_token})

    def test_login_user(self, prefix, test_client):
        """login user for fresh_token and check status in case of login"""
        response_login_user = test_client.post(
            f"{prefix}/user/login",
            headers={
                "Authorization": f"Bearer {TestUserBehaviour.token_dict['register_token']}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps({"email": "john1223@gmail.com", "password": PASSWORD}),
            follow_redirects=True,
        )

        fresh_access_token_login = json.loads(response_login_user.data)[
            "fresh_access_token"
        ]

        assert isinstance(fresh_access_token_login, str)
        assert response_login_user.status_code == 200
        TestUserBehaviour.token_dict.update(
            {"fresh_access_token_login": fresh_access_token_login}
        )

    def test_password_change_without_preconditions(self, prefix, test_client):
        """Changing password without preconditons"""
        fresh_token = TestUserBehaviour.token_dict["fresh_access_token_login"]
        response_password_change = test_client.put(
            f"{prefix}/user/changePassword",
            headers={
                "Authorization": f"Bearer {fresh_token}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps({"new_password": "1212312"}),
        )
        assert response_password_change.status_code == 412

    def test_password_change_without_fresh_token(self, prefix, test_client, session):
        """
        Test case to change password without fresh access token
        """
        response_password_change = test_client.put(
            f"{prefix}/user/changePassword",
            headers={
                "Authorization": f"Bearer {session}",
                "Content-Type": "application/json",
            },
            data=json.dumps({"new_password": "7897!!@@AB"}),
        )
        assert response_password_change.status_code == 401
        assert (
            json.loads(response_password_change.data)["message"]
            == "Fresh token required"
        )

    def test_register_user_without_token(self, prefix, test_client):
        """
        Test case to check user register without authentication token
        """
        response_register_user = test_client.post(
            f"{prefix}/user/register",
            data=json.dumps({"email": "john12@gmail.com", "password": "123!!@@AB"}),
        )
        assert response_register_user.status_code == 401

    def test_register_precondition_password(self, prefix, test_client, session):
        """
        Test case to check preconditions applied on password on userregister
        """
        register_user = test_client.post(
            f"{prefix}/user/register",
            headers={
                "Authorization": f"Bearer {session}",
                "Content-Type": "application/json",
            },
            data=json.dumps({"email": "john1234@gmail.com", "password": "12378"}),
        )
        assert register_user.status_code == 412

    def test_password_change_successfully(self, prefix, test_client):
        """password change successful case """
        fresh_token = TestUserBehaviour.token_dict["fresh_access_token_login"]
        response_password_change = test_client.put(
            f"{prefix}/user/changePassword",
            headers={
                "Authorization": f"Bearer {fresh_token}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps({"new_password": "7897!!@@AB"}),
            follow_redirects=True,
        )
        assert response_password_change.status_code == 200


class TestRepeatedCases:
    """
    common cases for test by user
    """

    token_dict = {}

    def test_start_session_success(self, prefix, test_client):
        """session start success case"""
        response_start_session = test_client.post(
            f"{prefix}/auth/startSession",
            headers={
                "Client-App-Token": "0b0069c752ec18172c5f782\
                08f1863d7ad6755a6fae6fe76ec2c80d13be41e42",
                "Timestamp": "1311231",
                "Device-ID": "1322a31x121za",
            },
        )

        assert (
            "access_token"
            and "refresh_token" in json.loads(response_start_session.data).keys()
        )

    def test_register_user_success(self, prefix, test_client, session):
        """register user success case"""
        response_register_user = test_client.post(
            f"{prefix}/user/register",
            headers={
                "Authorization": f"Bearer {session}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps({"email": "john12211a3@gmail.com", "password": PASSWORD}),
            follow_redirects=True,
        )
        access_token = json.loads(response_register_user.data)["access_token"]
        assert response_register_user.status_code == 201
        assert "access_token" in json.loads(response_register_user.data).keys()
        TestRepeatedCases.token_dict.update({"register_token": access_token})

    def test_login_user_success(self, prefix, test_client):
        """valid login case """
        response_login_user = test_client.post(
            f"{prefix}/user/login",
            headers={
                "Authorization": f"Bearer {TestRepeatedCases.token_dict['register_token']}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps({"email": "john12211a3@gmail.com", "password": PASSWORD}),
            follow_redirects=True,
        )

        fresh_access_token_login = json.loads(response_login_user.data)[
            "fresh_access_token"
        ]

        assert isinstance(fresh_access_token_login, str)
        assert response_login_user.status_code == 200
        assert "fresh_access_token" in json.loads(response_login_user.data).keys()
