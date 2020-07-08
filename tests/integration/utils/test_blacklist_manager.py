"""black_manager test"""
import fakeredis
from redis.exceptions import ConnectionError as RedisConnection
from src.utils.blacklist_manager import BlacklistManager
from src.utils.constant.response_messages import REDIS_CONNECTION

from ..mock_data import MockDataManager


class TestBlackListManager:
    """all test related to BlackList_manager file"""

    config = {}

    def test_content_data(self, data):
        """content data test"""
        mock_data_manager = MockDataManager(data)
        data.content.return_value = "TestBlackListManager"
        content_data = mock_data_manager.get_content()
        assert isinstance(content_data, dict)
        self.config.update(content_data)

    def test_blacklist_manager(self):
        """fake redis test"""

        blacklist_manager = BlacklistManager()
        seconds = self.config["JWT_ACCESS_TOKEN_EXPIRES_SECONDS"]
        blacklist_manager.revoke_token(self.config.get("key"), self.config.get("value"), seconds)
        black_list = blacklist_manager.get_jti_list()
        assert isinstance(black_list, list)

    def test_redis_failure(self):
        """connection test"""

        try:
            BlacklistManager.initialize_redis(app_config=self.config)
            BlacklistManager().revoke_token(self.config.get("key"), self.config.get("value"), self.config.get("JWT_ACCESS_TOKEN_EXPIRES_SECONDS"))
        except RedisConnection as error:
            assert str(error) == REDIS_CONNECTION

    def test_fake_redis(self):
        """fake redis test"""

        BlacklistManager.initialize_redis(fake_redis=fakeredis.FakeStrictRedis())
        token_revoke_status = BlacklistManager().revoke_token(
            self.config.get("key"), self.config.get("value"), self.config["JWT_ACCESS_TOKEN_EXPIRES_SECONDS"]
        )
        assert BlacklistManager().get_jti_list().__len__() > 0
        assert token_revoke_status
