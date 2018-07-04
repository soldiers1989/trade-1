"""
    http session
"""
import uuid
from app.aim import redis


class _Session:
    def __init__(self, id, redis):
        self._id = id
        self._redis = redis

    @property
    def id(self):
        return self._id

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
        else:
            val = val.decode()
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
    return 'ss_'+str(uuid.uuid4())


# redis for session
_sredis = redis.aim

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

