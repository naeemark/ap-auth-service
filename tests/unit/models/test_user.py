"""
    A file to containe all unit tests of
    UserModel
"""
import datetime
import os

import fakeredis
from redis.exceptions import ConnectionError as RedisConnection
from src import create_app
from src.models.user import UserModel
from src.utils.blacklist_manager import BlacklistManager
from src.utils.constant.response_messages import REDIS_CONNECTION


def context():
    """unit test instance for app and redis"""
    redis_instance = fakeredis.FakeStrictRedis()
    flask_app = create_app("flask_test.cfg")
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
        minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"])
    )
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(
        days=int(os.environ["JWT_REFRESH_TOKEN_EXPIRES_DAYS"])
    )
    return flask_app, redis_instance


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


def test_all_methods_present():
    """test methods """
    list_of_methods = new_user().__dir__()
    assert "save_to_db" in list_of_methods
    assert "find_by_email" in list_of_methods
    assert "find_by_id" in list_of_methods
    assert "delete_from_db" in list_of_methods


def test_blacklist_manager():
    """fake redis test"""
    test_context = context()
    blacklist_manager = BlacklistManager()
    seconds = test_context[0].config["JWT_ACCESS_TOKEN_EXPIRES"].seconds
    blacklist_manager.revoke_token("3", "1231231Xdfwefwe", seconds)
    black_list = blacklist_manager.get_jti_list()
    assert isinstance(black_list, list)


def test_jwt_life_span():
    """life span check"""
    test_context = context()

    token_expire_seconds = test_context[0].config["JWT_ACCESS_TOKEN_EXPIRES"].seconds
    refresh_token_expire_days = test_context[0].config["JWT_REFRESH_TOKEN_EXPIRES"].days

    assert token_expire_seconds / 60 == int(os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"])
    assert refresh_token_expire_days == int(os.environ["JWT_REFRESH_TOKEN_EXPIRES_DAYS"])


def test_redis():
    """fake redis test"""
    redis_instance = fakeredis.FakeStrictRedis()
    redis_instance.set("1", "abc")
    redis_instance.set("test", "12")

    assert redis_instance.get("test").decode() == "12"
    assert redis_instance.get("1").decode() == "abc"


def test_redis_failure():
    """connection test"""
    test_context = context()

    test_context[0].config["ENV"] = "redis_test"
    try:
        BlacklistManager.initialize_redis(test_context[0].config)
        BlacklistManager().revoke_token("121", "113123131", test_context[0].config["JWT_ACCESS_TOKEN_EXPIRES"].seconds)
    except RedisConnection as error:
        assert str(error) == REDIS_CONNECTION


def test_fake_redis():
    """fake redis test"""
    test_context = context()

    BlacklistManager.initialize_redis(test_context[0].config)
    token_revoke_status = BlacklistManager().revoke_token(
        "121", "113123131", test_context[0].config["JWT_ACCESS_TOKEN_EXPIRES"].seconds
    )
    assert BlacklistManager().get_jti_list().__len__() > 0
    assert token_revoke_status
