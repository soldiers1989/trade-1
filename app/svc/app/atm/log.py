"""
    log for aim
"""
from app.atm import redis


class _RedisLog:
    def __init__(self, name, redis, maxrecords = 1000):
        """
            init a redis log
        :param name:
        :param redis:
        """
        self._name = name
        self._redis = redis
        self._maxrecords = maxrecords

    def log(self, msg):
        """
            log error message
        :param msg:
        :return:
        """
        self._redis.lpush(self._name, msg)

        if self._redis.llen(self._name) > self._maxrecords:
            self._redis.rpop(self._name)

    def get(self, wantrecords=20):
        """
            get latest want records
        :param wantrecords: int, number records want
        :return:
        """
        records = []
        num = 0
        while num < wantrecords:
            record = self._redis.lindex(self._name, num)
            if record is None:
                break
            records.append(record)
            num += 1

        return records

# info log object
_infolog = _RedisLog('log_atm_info', redis.log)


# error log object
_errorlog = _RedisLog('log_atm_error', redis.log)


def info(msg):
    try:
        # log to console
        print(msg)

        # log to redis
        _infolog.log(msg)
    except:
        pass


def getinfo(wantrecords=20):
    try:
        return _errorlog.get(wantrecords)
    except:
        return ""


def error(msg):
    try:
        # log to console
        print(msg)

        # log to redis
        _errorlog.log(msg)
    except:
        pass


def geterror(wantrecords=20):
    try:
        return _errorlog.get(wantrecords)
    except:
        return ""