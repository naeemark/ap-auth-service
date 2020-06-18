"""
blacklist file to handle logout
"""
import os

import fakeredis
from redis import exceptions
from redis import Redis
from redis.exceptions import ConnectionError as RedisConnection


class BlacklistManager:
    """
     managing tokens which are revoked
    """

    __redis_instance = None

    def __init__(self):
        self.redis = self.__redis_instance

    def insert_blacklist_token_id(self, identity, jti, expire_time_sec):
        """
        :param identity: identity
        :param jti: JWT ID
        :return: bool status
        """
        try:
            # To-do: need to discuss the logic
            return self.redis.set(str(jti), str(identity), str(expire_time_sec))
        except RedisConnection as error:
            raise error

    def get_jti_list(self):
        """
        :return: list of jti
        """
        try:
            return list(map(self.decode_jti, self.redis.keys()))
        except (AttributeError, RedisConnection):
            # To-do discuss the exception and return
            return []

    def decode_jti(self, encoded_jti):
        """
        :param encoded_jti: jti value
        :return: decoded jti value
        """
        return encoded_jti.decode()

    @classmethod
    def initialize_redis(cls, app_config):
        """initialize redis config"""

        if app_config["ENV"] == "testing":
            cls.__redis_instance = fakeredis.FakeStrictRedis()
        else:
            try:
                host, port = os.environ.get("REDIS_HOST"), os.environ.get("REDIS_PORT")
                redis_instance = Redis(host=host, port=port)
                redis_instance.ping()
                cls.__redis_instance = redis_instance
                print("Connected to redis at {}:{}".format(host, port))
            except exceptions.ConnectionError as redis_connection_error:
                print("Redis:", redis_connection_error)
