"""
    A file to contain all unit tests of
    UserModel
"""
from src.models.user import UserModel


def new_user():
    """
        Creates and return new User
    """
    user = UserModel(email="abc123@gmail.com", password="FlaskIsAwesome", name="Flask Developer")
    return user


def test_new_user():
    """
        Validates newly created User
    """
    # pylint: disable=redefined-outer-name

    assert new_user() is not None
    assert new_user().email == "abc123@gmail.com"
    assert new_user().password == "FlaskIsAwesome"
    assert new_user().name == "Flask Developer"


def test_json_user_model():
    """test json function """

    assert isinstance(new_user().dict(), dict)
