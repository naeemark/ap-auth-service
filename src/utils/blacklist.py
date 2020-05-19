"""
blacklist file to handle logout
"""
import redis
import os


class BlacklistManager():
    def __init__(self):
        self.redis = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])

    def insert_blacklist_token_id(self, identity, jti, expire_in_min=15):
        """
        :param identity: identity
        :param jti: JWT ID
        :param expire_in_min: by default JWT_ACCESS_TOKEN_EXPIRES has 15min time
        :return: bool status
        """
        expire_time = expire_in_min * 60
        return self.redis.set(str(jti), str(identity), str(expire_time))

    def get_jti_list(self):
        """
        :return: list of jti
        """
        decode_jti = lambda jti: jti.decode()
        jti_list = list(map(decode_jti, self.redis.keys()))
        return jti_list
