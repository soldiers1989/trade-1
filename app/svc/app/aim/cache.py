"""
    sms manager
"""
from . import redis


# cache storage with get/set
class _Cache:
    def __init__(self, redis):
        """
            init cache storage with redis object
        :param redis:
        """
        self._redis = redis

    def set(self, key, data, expires):
        """
            set cache data by key
        :param key:
        :param data:
        :param expires:
        :return:
        """
        self._redis.setex(key, data, expires)

    def get(self, key):
        """
            get cache data by key
        :param key:
        :return:
        """
        return self._redis.get(key)


# default cache object
default = _Cache(redis.cache)
