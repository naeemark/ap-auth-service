"""
    A file to containe all unit tests of
    UserModel
"""
from src.models.user import UserModel


def new_user():
    """
        Creates and return new User
    """
    user = UserModel("abc123@gmail.com", "FlaskIsAwesome")
    return user


def test_new_user():
    """
        Validates newly created User
    """
    # pylint: disable=redefined-outer-name

    assert new_user() is not None
    assert new_user().email == "abc123@gmail.com"
    assert new_user().password == "FlaskIsAwesome"


def test_json_user_model():
    """test json function """

    assert isinstance(new_user().json(), dict)
