"""
blacklist file to handle logout
"""


class BlacklistManager:
    """
     managing tokens which are revoked
    """

    redis_instance = None
    token_expire_seconds = None

    def __init__(self):
        self.redis = BlacklistManager.redis_instance

    def insert_blacklist_token_id(self, identity, jti):
        """
        :param identity: identity
        :param jti: JWT ID
        :return: bool status
        """
        expire_time = BlacklistManager.token_expire_seconds
        return self.redis.set(str(jti), str(identity), str(expire_time))

    def get_jti_list(self):
        """
        :return: list of jti
        """

        jti_list = list(map(self.decode_jti, self.redis.keys()))
        return jti_list

    def decode_jti(self, encoded_jti):
        """
        :param encoded_jti: jti value
        :return: decoded jti value
        """
        return encoded_jti.decode()

    @classmethod
    def initialize_redis(cls, token_expire_seconds, redis_instance):
        """initialize redis config"""

        cls.redis_instance = redis_instance
        cls.token_expire_seconds = token_expire_seconds
