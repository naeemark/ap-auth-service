"""
    A configuration file for pytest integration testing
"""
import os

import bcrypt
import pytest
from flask_jwt_extended import JWTManager
from src import create_app
from src import db
from src.models.user import UserModel
from src.resources import initialize_resources


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
    initialize_resources(flask_app)
    JWTManager(flask_app)

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


