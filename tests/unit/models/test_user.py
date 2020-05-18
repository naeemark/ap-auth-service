"""
    A file to containe all unit tests of
    UserModel
"""
import pytest
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



