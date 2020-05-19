"""
blacklist file to handle logout
"""
import redis


class RedisManager():
    def __init__(self, port, host):
        self.redis = redis.Redis(host=host, port=port)

    def insert_blacklist_token_id(self, identity, jti, expire_in_min=15):
        expire_time = expire_in_min * 60
        return self.redis.set(str(jti), str(identity), str(expire_time))

    def get_jti_list(self):
        decode_jti = lambda jti: jti.decode()
        jti_list = list(map(decode_jti, self.redis.keys()))
        return jti_list
