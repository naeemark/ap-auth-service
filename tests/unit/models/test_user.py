"""
    A file to containe all unit tests of
    UserModel
"""
import pytest
import json

from src.models.user import UserModel


@pytest.fixture(scope="module")
def new_user():
    """
        Creates and return new User
    """
    user = UserModel("abc123@gmail.com", "FlaskIsAwesome")
    return user


def test_new_user(new_user):
    """
        Validates newly created User
    """
    # pylint: disable=redefined-outer-name
    assert new_user is not None
    assert new_user.email == "abc123@gmail.com"
    assert new_user.password == "FlaskIsAwesome"


def test_register_user_without_token(api_prefix, test_client, test_database):
    """
    Test case to check user register without authentication token
    """
    test_database
    response_register_user = test_client.post(
        f"{api_prefix}/user/register",
        data=json.dumps({'email': 'john12@gmail.com', 'password': '123!!@@AB'})
    )
    assert response_register_user.status_code == 401


def test_register_precondition_password(api_prefix, test_client, test_database):
    """
    Test case to check preconditions applied on password on user register
    """
    test_database
    response_start_session = test_client.post(
        f"{api_prefix}/auth/StartSession",
        headers={'Client-App-Token': '0b0069c752ec14172c5f78208f1863d7ad6755a6fae6fe76ec2c80d13be41e42',
                 'Timestamp': '131231', 'Device-ID': '1321a31x121za'}
    )
    access_token_session = json.loads(response_start_session.data)['access_token']

    response_register_user = test_client.post(
        f"{api_prefix}/user/register", headers={
            'Authorization': f'Bearer {access_token_session}',
            'Content-Type': 'application/json'
        }, data=json.dumps({'email': 'john12@gmail.com', 'password': '12378'}))
    assert response_register_user.status_code == 412


def test_start_session_generated_tokens(api_prefix, test_client, test_database):
    """
    Test case to check tokens generated by startSession
    """
    test_database
    response_start_session = test_client.post(
        f"{api_prefix}/auth/StartSession", headers={
            'Client-App-Token': '0b0069c752ec14172c5f78208f1863d7ad6755a6fae6fe76ec2c80d13be41e42',
            'Timestamp': '131231',
            'Device-ID': '1321a31x121za'})
    assert response_start_session.status_code == 200
    assert 'access_token' and 'refresh_token' in json.loads(response_start_session.data).keys()
