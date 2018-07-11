"""
    http session
"""
import time
from app.aim import redis
from app.util import rand


class _Session:
    """
        user session
    """
    def __init__(self, id, redis):
        self._id = id
        self._redis = redis

        if self._redis.exists(self._id):
            self.set('ctime', time.time())

    @property
    def id(self):
        return self._id

    def create(self):
        """
            create s
        :return:
        """

    def set(self, key, val):
        """
            set session value
        :param key:
        :param val:
        :return:
        """
        self._redis.hset(self._id, key, val)

    def get(self, key, default=None):
        """
            get session value
        :param key:
        :param default:
        :return:
        """
        val = self._redis.hget(self._id, key)
        if val is None:
            val = default

        return val

    def all(self):
        """
            get all session data
        :return:
        """
        val = self._redis.hgetall(self._id)
        return val

    def clear(self):
        """
            clear session
        :return:
        """
        self._redis.delete(self._id)

    def expire(self, seconds):
        """
            reset session expire time in seconds
        :param seconds:
        :return:
        """
        try:
            if self._redis.exists(self._id):
                self._redis.expire(self._id, seconds)
        except:
            pass


def _newid():
    """
        create new session id
    :return:
    """
    return rand.uuid()


# redis for session
_sredis = redis.session

# get session by id
def get(sid = None):
    """
        get a session object by id
    :param sid:
    :return:
    """
    if sid is None:
        sid = _newid()

    return _Session(sid, _sredis)

