# pylint: disable=unused-argument
"""
    A file to containe all integration tests of
    UserResource
"""


def test_sum(test_client, test_database):
    """
        A sample test to demostrate the availability of test_client and test_dataabase
    """
    # for mock purpose
    assert 1 + 1 == 2


def test_register_login_routes(api_prefix, test_client, test_database):
    """
       Integration test for User Register and Login flows
       - Best Case Scenarios
    """
    register = test_client.post(
        f"{api_prefix}/user/register",
        data={"email": "abc1@xyz.com", "password": "1234567A@"},
        follow_redirects=True,
    )
    assert register.status_code == 201

    login = test_client.post(
        f"{api_prefix}/user/login",
        data={"email": "abc1@xyz.com", "password": "1234567A@"},
        follow_redirects=True,
    )
    assert login.status_code == 200
