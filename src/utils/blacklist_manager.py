"""
blacklist file to handle logout
"""
from redis import exceptions
from redis import Redis
from redis.exceptions import ConnectionError as RedisConnection
from src.utils.constant.response_messages import REDIS_CONNECTION


class BlacklistManager:
    """
     managing tokens which are revoked
    """

    __redis_instance = None

    def __init__(self):
        self.redis = self.__redis_instance

    def revoke_token(self, identity, jti, expire_time_sec):
        """
        :param identity: identity
        :param jti: JWT ID
        :return: bool status
        """
        try:
            return self.redis.set(str(jti), str(identity), str(expire_time_sec))
        except AttributeError:
            raise RedisConnection(REDIS_CONNECTION)

    def get_jti_list(self):
        """
        :return: list of jti
        """
        try:
            return list(map(self.decode_jti, self.redis.keys()))
        except (AttributeError, RedisConnection):
            return []

    def decode_jti(self, encoded_jti):
        """
        :param encoded_jti: jti value
        :return: decoded jti value
        """
        return encoded_jti.decode()

    @classmethod
    def initialize_redis(cls, app_config=None, fake_redis=None):
        """initialize redis config"""

        if fake_redis:
            cls.__redis_instance = fake_redis
        else:
            try:
                host, port = app_config["REDIS_HOST"], app_config["REDIS_PORT"]
                redis_instance = Redis(host=host, port=port)
                redis_instance.ping()
                cls.__redis_instance = redis_instance
                print("Connected to redis at {}:{}".format(host, port))
            except exceptions.ConnectionError as redis_connection_error:
                print("Redis:", redis_connection_error)
            except AttributeError as error:
                print("AttributeError:", error)
