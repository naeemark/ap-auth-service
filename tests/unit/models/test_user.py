import pytest
from src.models.user import UserModel as User


@pytest.fixture(scope="module")
def new_user():
    user = User("abc123@gmail.com", "FlaskIsAwesome")
    return user


def test_new_user(new_user):
    assert new_user is not None
    assert new_user.email == "abc123@gmail.com"
    assert new_user.password == "FlaskIsAwesome"
