"""
    redis wrapper
"""
import redis


class MyRedis:
    def __init__(self, cfg):
        """
            init redis object by configure
        :param cfg:
        """
        # connection pool
        self._pool = redis.ConnectionPool(**cfg)

    def get(self):
        """
            get a redis object
        :return:
        """
        return redis.Redis(connection_pool=self._pool)
