"""
    A configuration file for pytest integration testing
"""
import json
import os

import bcrypt
import pytest
from flask_jwt_extended import JWTManager
from mock import Mock
from src import create_app
from src import db
from src.models.user import UserModel
from src.resources import initialize_resources
from tests.integration.mock_data import MockData
from tests.integration.mock_data import MockDataManager


@pytest.fixture(scope="module")
def new_user():
    """
        Creates a new user
    """
    user = UserModel("patkennedy79@gmail.com", "FlaskIsAwesome")
    return user


@pytest.fixture(scope="module")
def test_client():
    """
        Configure and provides app-client instance for testing
    """
    flask_app = create_app("flask_test.cfg")
    jwt = JWTManager(flask_app)
    initialize_resources(flask_app, jwt)

    db.init_app(flask_app)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # # Establish an application context before running the tests.
    context = flask_app.app_context()
    context.push()

    yield testing_client  # this is where the testing happens!

    context.pop()

    # Delete test database file after execution
    os.remove(flask_app.config["SQLALCHEMY_DATABASE_URI"].split("///")[-1])


@pytest.fixture(scope="module")
def test_database():
    """
        Configure and provides database instance for testing
    """

    try:
        # Create the database and the database table
        db.create_all()

        # create user data objects
        user1 = UserModel(
            email="abc@gmail.com", password=bcrypt.hashpw(b"123abc@", bcrypt.gensalt())
        )
        user2 = UserModel(
            email="abcd@gmail.com",
            password=bcrypt.hashpw(b"PaSsWoRd", bcrypt.gensalt()),
        )

        # Add users to database
        db.session.add(user1)
        db.session.add(user2)

        # Commit the changes for the users
        db.session.commit()

        yield db  # this is where the testing happens!

        db.session.close()
        db.drop_all()
    # pylint: disable=broad-except
    except Exception as exception:
        print(exception)


@pytest.yield_fixture()
def data():
    """returns the data sepicified earlier"""
    return Mock(spec=MockData)


@pytest.fixture(scope="module")
def api_prefix(test_client):
    """
        Find and returns API_PREFIX for all integration tests
    """
    # pylint: disable=redefined-outer-name
    return (
        test_client.application.config["API_PREFIX"]
        if "API_PREFIX" in test_client.application.config
        else ""
    )


@pytest.yield_fixture()
def session(api_prefix, test_client, data):
    """
        Generates session response
    """
    # pylint: disable=redefined-outer-name
    mock_data_manager = MockDataManager(data)
    data.content.return_value = "base_startSession"
    response_start_session = test_client.post(
        f"{api_prefix}/auth/startSession",
        headers=mock_data_manager.get_content()["headers"],
    )
    tokens = json.loads(response_start_session.data)
    return tokens["access_token"], tokens["refresh_token"]


@pytest.yield_fixture()
def register_token(api_prefix, test_client, session, data):
    """
        Generates token after register
    """
    # pylint: disable=redefined-outer-name
    mock_data_manager = MockDataManager(data)
    data.content.return_value = "register_user_1"

    response_register_user = test_client.post(
        f"{api_prefix}/user/register",
        headers={
            "Authorization": f" {session[0]}",
            "Content-Type": "application/json",
        },
        data=json.dumps(mock_data_manager.get_content()["data"]),
        follow_redirects=True,
    )

    return json.loads(response_register_user.data)["access_token"]
