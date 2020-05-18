"""
    A configuration file for pytest integration testing
"""
import bcrypt
import pytest
from src import create_app
from src import db
from src.models.user import UserModel
from src.app import app


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

    # update cfg file for test
    app.config.from_pyfile("flask_test.cfg")

    flask_app = app
    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()
        # Flask provides a way to test your application by exposing the Werkzeug test Client
        # and handling the context locals for you.
        testing_client = flask_app.test_client()

        # # Establish an application context before running the tests.
        context = flask_app.app_context()
        context.push()

        yield testing_client  # this is where the testing happens!
        db.session.remove()
        db.drop_all()
        context.pop()


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
        db.session.remove()
        db.drop_all()
    # pylint: disable=broad-except
    except Exception as exception:
        print(exception)
