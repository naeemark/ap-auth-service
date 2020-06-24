"""
    A file to containe all unit tests of
    UserModel
"""
import fakeredis
from redis.exceptions import ConnectionError as RedisConnection
from src.models.user import UserModel
from src.utils.blacklist_manager import BlacklistManager
from src.utils.constant.response_messages import REDIS_CONNECTION


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
    config = {
        "JWT_ACCESS_TOKEN_EXPIRES_SECONDS": 1800,
    }
    blacklist_manager = BlacklistManager()
    seconds = config["JWT_ACCESS_TOKEN_EXPIRES_SECONDS"]
    blacklist_manager.revoke_token("3", "1231231Xdfwefwe", seconds)
    black_list = blacklist_manager.get_jti_list()
    assert isinstance(black_list, list)


def test_redis():
    """fake redis test"""
    redis_instance = fakeredis.FakeStrictRedis()
    redis_instance.set("1", "abc")
    redis_instance.set("test", "12")

    assert redis_instance.get("test").decode() == "12"
    assert redis_instance.get("1").decode() == "abc"


def test_redis_failure():
    """connection test"""

    config = {
        "ENV": "redis_test",
        "JWT_ACCESS_TOKEN_EXPIRES_SECONDS": 1800,
        "REDIS_HOST": "127.0.0.1",
        "REDIS_PORT": "6319",
    }
    try:
        BlacklistManager.initialize_redis(config)
        BlacklistManager().revoke_token("121", "113123131", config.get("JWT_ACCESS_TOKEN_EXPIRES_SECONDS"))
    except RedisConnection as error:
        assert str(error) == REDIS_CONNECTION


def test_fake_redis():
    """fake redis test"""
    config = {
        "ENV": "testing",
        "JWT_ACCESS_TOKEN_EXPIRES_SECONDS": 1800,
    }
    BlacklistManager.initialize_redis(config)
    token_revoke_status = BlacklistManager().revoke_token(
        "121", "113123131", config["JWT_ACCESS_TOKEN_EXPIRES_SECONDS"]
    )
    assert BlacklistManager().get_jti_list().__len__() > 0
    assert token_revoke_status
