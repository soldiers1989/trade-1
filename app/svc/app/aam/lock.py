"""
    lock for business
"""
import time
from . import myredis


class _LockException(Exception):
    def __init__(self):
        Exception.__init__(self, '用户正在操作，请稍后重试')


class _Lock:
    def __init__(self, type, id):
        self._key = 'lock_%s_%s' % (type, str(id))

    def __enter__(self):
        """
            lock user by user id
        :param userid:
        :return:
        """
        if myredis.lock.get(self._key) is not None:
            raise _LockException()

        myredis.lock.set(self._key, time.time())

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            unlock user by user id
        :param userid:
        :return:
        """
        myredis.lock.delete(self._key)


def user(userid):
    """
        create user lock object
    :param userid:
    :return:
    """
    return _Lock('user', userid)


def order(orderid):
    """
        create order lock object
    :param orderid:
    :return:
    """
    return _Lock('order', orderid)