# pylint: disable=unused-argument
"""
    A file to containe all integration tests of
    UserResource
"""
import json

from ..mock_data import MockDataManager


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

    def test_login_user(self, prefix, test_client, data):
        """login user for fresh_token and check status in case of login"""

        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestUserBehaviour"

        response_login_user = test_client.post(
            f"{prefix}/user/login",
            headers={
                "Authorization": f"Bearer {TestUserBehaviour.token_dict['register_token']}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps(mock_data_manager.get_content()["login"]["data"]),
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

    def test_password_change_without_preconditions(self, prefix, test_client, data):
        """Changing password without preconditons"""
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestUserBehaviour"

        fresh_token = TestUserBehaviour.token_dict["fresh_access_token_login"]
        response_password_change = test_client.put(
            f"{prefix}/user/changePassword",
            headers={
                "Authorization": f"Bearer {fresh_token}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps(
                mock_data_manager.get_content()["changePassword_precondition"]["data"]
            ),
        )
        assert response_password_change.status_code == 412

    def test_password_change_without_fresh_token(
        self, prefix, test_client, session, data
    ):
        """
        Test case to change password without fresh access token
        """
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestUserBehaviour"

        response_password_change = test_client.put(
            f"{prefix}/user/changePassword",
            headers={
                "Authorization": f"Bearer {session}",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                mock_data_manager.get_content()["changePassword_no_fresh_token"]["data"]
            ),
        )
        assert response_password_change.status_code == 401
        assert (
            json.loads(response_password_change.data)["message"]
            == "Fresh token required"
        )

    def test_register_user_without_token(self, prefix, test_client, data):
        """
        Test case to check user register without authentication token
        """
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestUserBehaviour"
        response_register_user = test_client.post(
            f"{prefix}/user/register",
            data=json.dumps(
                mock_data_manager.get_content()["register_without_token"]["data"]
            ),
        )
        assert response_register_user.status_code == 401

    def test_register_precondition_password(self, prefix, test_client, session, data):
        """
        Test case to check preconditions applied on password on userregister
        """
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestUserBehaviour"
        register_user = test_client.post(
            mock_data_manager.get_content()["register_precondition_password"][
                "url"
            ].format(prefix=prefix),
            headers={
                "Authorization": f"Bearer {session}",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                mock_data_manager.get_content()["register_precondition_password"][
                    "data"
                ]
            ),
        )
        assert register_user.status_code == 412

    def test_password_change(self, prefix, test_client, data):
        """password change case """
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestUserBehaviour"

        fresh_token = TestUserBehaviour.token_dict["fresh_access_token_login"]
        response_password_change = test_client.put(
            f"{prefix}/user/changePassword",
            headers={
                "Authorization": f"Bearer {fresh_token}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps(mock_data_manager.get_content()["password_change"]["data"]),
            follow_redirects=True,
        )
        assert response_password_change.status_code == 200


class TestRepeatedCases:
    """
    common cases for test by user
    """

    token_dict = {}

    def test_start_session_success(self, prefix, test_client, data):
        """session start success case"""
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestRepeatedCases"
        response_start_session = test_client.post(
            f"{prefix}/auth/startSession",
            headers=mock_data_manager.get_content()["start_session"]["headers"],
        )

        assert (
            "access_token"
            and "refresh_token" in json.loads(response_start_session.data).keys()
        )

    def test_register_user_success(self, prefix, test_client, session, data):
        """register user success case"""
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestRepeatedCases"
        response_register_user = test_client.post(
            f"{prefix}/user/register",
            headers={
                "Authorization": f"Bearer {session}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps(mock_data_manager.get_content()["user_register"]["data"]),
            follow_redirects=True,
        )
        access_token = json.loads(response_register_user.data)["access_token"]
        assert response_register_user.status_code == 201
        assert "access_token" in json.loads(response_register_user.data).keys()
        TestRepeatedCases.token_dict.update({"register_token": access_token})

    def test_login_user_success(self, prefix, test_client, data):
        """valid login case """
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestRepeatedCases"

        response_login_user = test_client.post(
            f"{prefix}/user/login",
            headers={
                "Authorization": f"Bearer {TestRepeatedCases.token_dict['register_token']}",
                CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE,
            },
            data=json.dumps(mock_data_manager.get_content()["login"]["data"]),
            follow_redirects=True,
        )

        fresh_access_token_login = json.loads(response_login_user.data)[
            "fresh_access_token"
        ]

        assert isinstance(fresh_access_token_login, str)
        assert response_login_user.status_code == 200
        assert "fresh_access_token" in json.loads(response_login_user.data).keys()
