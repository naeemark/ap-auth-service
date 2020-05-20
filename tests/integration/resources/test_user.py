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


CONTENT_TYPE_KEY = 'Content-Type'
CONTENT_TYPE_VALUE = 'application/json'


def test_StartSession_flow(api_prefix, test_client, test_database):
    """
       Integration test for Start_Session and Login flows
       - Best Case Scenarios
    """

    response_start_session = test_client.post(
        f"{api_prefix}/auth/StartSession",
        headers=
        {
            'Client-App-Token': '0b0069c752ec14172c5f78208f1863d7ad6755a6fae6fe76ec2c80d13be41e42',
            'Timestamp': '131231',
            'Device-ID': '1321a31x121za'
        },
        follow_redirects=True
    )
    access_token_session = json.loads(response_start_session.data)['access_token']

    response_register_user = test_client.post(
        f"{api_prefix}/user/register",
        headers=
        {
            'Authorization': f'Bearer {access_token_session}',
            CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE
        },
        data=json.dumps({'email': 'john12@gmail.com', 'password': '123!!@@AB'}),
        follow_redirects=True,
    )

    access_token_register = json.loads(response_register_user.data)['access_token']

    response_login_user = test_client.post(
        f"{api_prefix}/user/login",
        headers=
        {
            'Authorization': f'Bearer {access_token_register}',
            CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE
        },
        data=json.dumps({'email': 'john12@gmail.com', 'password': '123!!@@AB'}),
        follow_redirects=True,
    )

    fresh_access_token_login = json.loads(response_login_user.data)['fresh_access_token']

    response_password_change = test_client.put(
        f"{api_prefix}/user/changePassword",
        headers=
        {
            'Authorization': f'Bearer {fresh_access_token_login}',
            CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE
        },
        data=json.dumps({'new_password': '7897!!@@AB'}),
        follow_redirects=True,
    )
    assert response_password_change.status_code == 200


def test_password_change_without_fresh_token(api_prefix, test_client, test_database):
    """
    Test case to change password without fresh access token
    """
    response_start_session = test_client.post(
        f"{api_prefix}/auth/StartSession",
        headers=
        {
            'Client-App-Token': '0b0069c752ec14172c5f78208f1863d7ad6755a6fae6fe76ec2c80d13be41e42',
            'Timestamp': '131231',
            'Device-ID': '1321a31x121za'
        },
        follow_redirects=True
    )
    access_token_session = json.loads(response_start_session.data)['access_token']

    response_password_change = test_client.put(
        f"{api_prefix}/user/changePassword",
        headers=
        {
            'Authorization': f'Bearer {access_token_session}',
            'Content-Type': 'application/json'
        },
        data=json.dumps({'new_password': '7897!!@@AB'})
    )
    assert response_password_change.status_code == 401
    assert json.loads(response_password_change.data)['message'] == 'Fresh token required'


def test_password_change_without_preconditions(api_prefix, test_client, test_database):
    """
    Test case to change password without preconditions
    """
    response_start_session = test_client.post(
        f"{api_prefix}/auth/StartSession",
        headers=
        {
            'Client-App-Token': '0b0069c752fc14172c5f78208f1863d7ad6755a6fae6fe76ec2c80d13be41e42',
            'Timestamp': '131231',
            'Device-ID': '1321a31x121za'
        },
        follow_redirects=True
    )
    access_token_session = json.loads(response_start_session.data)['access_token']

    response_register_user = test_client.post(
        f"{api_prefix}/user/register",
        headers=
        {
            'Authorization': f'Bearer {access_token_session}',
            CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE
        },
        data=json.dumps({'email': 'john123@gmail.com', 'password': '123!!@@AB'}),
        follow_redirects=True,
    )

    access_token_register = json.loads(response_register_user.data)['access_token']

    response_login_user = test_client.post(
        f"{api_prefix}/user/login",
        headers=
        {
            'Authorization': f'Bearer {access_token_register}',
            CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE
        },
        data=json.dumps({'email': 'john123@gmail.com', 'password': '123!!@@AB'}),
        follow_redirects=True,
    )

    fresh_access_token_login = json.loads(response_login_user.data)['fresh_access_token']

    response_password_change = test_client.put(
        f"{api_prefix}/user/changePassword",
        headers=
        {
            'Authorization': f'Bearer {fresh_access_token_login}',
            CONTENT_TYPE_KEY: CONTENT_TYPE_VALUE
        },
        data=json.dumps({'new_password': '1212312'}),
    )
    assert response_password_change.status_code == 412
