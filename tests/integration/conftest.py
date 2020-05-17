import bcrypt
import pytest
from src import create_app
from src import db
from src.models.user import UserModel


@pytest.fixture(scope="module")
def new_user():
    user = UserModel("patkennedy79@gmail.com", "FlaskIsAwesome")
    return user


@pytest.fixture(scope="module")
def test_client():

    flask_app = create_app("flask_test.cfg")
    db.init_app(flask_app)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # # Establish an application context before running the tests.
    context = flask_app.app_context()
    context.push()

    yield testing_client  # this is where the testing happens!

    context.pop()


@pytest.fixture(scope="module")
def test_database(test_client):

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

        db.drop_all()
    except Exception as e:
        print(e)
