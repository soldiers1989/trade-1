"""
    lock for business
"""
import time
from app.aam import redis


class _LockException(Exception):
    def __init__(self):
        Exception.__init__(self, '操作频繁，请稍后重试')

exception = _LockException


class _UserLock:
    def __init__(self, userid):
        self._key = 'lock_' + userid

    def __enter__(self):
        """
            lock user by user id
        :param userid:
        :return:
        """
        if redis.lock.get(self._key) is not None:
            raise exception()

        redis.lock.set(self._key, time.time())

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            unlock user by user id
        :param userid:
        :return:
        """
        redis.lock.delete(self._key)


def user(userid):
    """
        create user lock object
    :param userid:
    :return:
    """
    return _UserLock(userid)
