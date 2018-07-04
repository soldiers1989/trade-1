"""
    http session
"""


class Session:
    def __init__(self):
        pass

    def set(self, key, val):
        pass

    def get(self, key, default=None):
        pass


class RedisSession:
    def __init__(self, redis):
        self._redis = redis


