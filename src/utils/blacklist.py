"""
blacklist file to handle logout
"""
import os

import redis

test_blacklist = []


class BlacklistManager:
    """
     managing tokens which are revoked
    """

    def __init__(self):
        self.redis = None
        if not os.environ.get("REDIS_HOST") and not os.environ.get("REDIS_PORT"):
            self.redis = test_blacklist
        else:
            self.redis = redis.Redis(
                host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"]
            )

    def insert_blacklist_token_id(self, identity, jti, expire_in_min=15):
        """
        :param identity: identity
        :param jti: JWT ID
        :param expire_in_min: by default JWT_ACCESS_TOKEN_EXPIRES has 15min time
        :return: bool status
        """
        if isinstance(self.redis, list):
            self.redis.append(str(jti))
            return True

        expire_time = expire_in_min * 60
        return self.redis.set(str(jti), str(identity), str(expire_time))

    def get_jti_list(self):
        """
        :return: list of jti
        """
        if isinstance(self.redis, list):
            return self.redis
        jti_list = list(map(self.decode_jti, self.redis.keys()))
        return jti_list

    def decode_jti(self, encoded_jti):
        """
        :param encoded_jti: jti value
        :return: decoded jti value
        """
        return encoded_jti.decode()
