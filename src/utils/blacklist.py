"""
blacklist file to handle logout
"""


class BlacklistManager:
    """
     managing tokens which are revoked
    """

    redis_config = {}

    def __init__(self):
        self.redis = BlacklistManager.redis_config.get("instance")

    def insert_blacklist_token_id(self, identity, jti):
        """
        :param identity: identity
        :param jti: JWT ID
        :return: bool status
        """
        expire_time = BlacklistManager.redis_config.get("TOKEN_EXPIRE")
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
    def initialize_redis(cls, app, redis_instance):
        """initialize redis config"""
        cls.redis_config.update(
            {
                "TOKEN_EXPIRE": app.config.get("JWT_ACCESS_TOKEN_EXPIRES").seconds,
                "instance": redis_instance,
            }
        )
