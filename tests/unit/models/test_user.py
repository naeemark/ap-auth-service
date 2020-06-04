"""
    A file to containe all unit tests of
    UserModel
"""
import datetime
import os

import fakeredis
from src import create_app
from src.models.user import UserModel
from src.utils.blacklist_manager import BlacklistManager


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


def test_blacklist_manager():
    """fake redis test"""
    redis_instance = fakeredis.FakeStrictRedis()
    flask_app = create_app("flask_test.cfg")
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
        minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"])
    )
    token_expire_seconds = flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"].seconds
    BlacklistManager.initialize_redis(token_expire_seconds, redis_instance)
    blacklist_manager = BlacklistManager()
    blacklist_manager.insert_blacklist_token_id("3", "1231231Xdfwefwe")
    black_list = blacklist_manager.get_jti_list()

    assert isinstance(black_list, list)


def test_redis():
    """fake redis test"""
    redis_instance = fakeredis.FakeStrictRedis()
    redis_instance.set("1", "abc")
    redis_instance.set("test", "12")

    assert redis_instance.get("test").decode() == "12"
    assert redis_instance.get("1").decode() == "abc"
