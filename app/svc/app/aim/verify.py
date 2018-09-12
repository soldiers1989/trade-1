"""
    verify code definition
"""
from . import redis


# image verify code storage with get/set
class _ImageVerify:
    def __init__(self, redis):
        """
            init verify storage with redis object
        :param redis:
        """
        self._redis = redis

    def set(self, id, code, expires):
        """
            save verify vode with id
        :param id:
        :param val:
        :return:
        """
        self._redis.setex(id, code, expires)

    def get(self, id):
        """
            get verify code by id
        :param id:
        :return:
        """
        return self._redis.get(id)

# image verify code object
image = _ImageVerify(redis.vimg)


# sms verify code storage with get/set
class _SmsVerify:
    def __init__(self, redis):
        """
            init verify storage with redis object
        :param redis:
        """
        self._redis = redis

    def set(self, phone, code, expires):
        """
            save verify vode with id
        :param id:
        :param val:
        :return:
        """
        self._redis.setex(phone, code, expires)

    def get(self, phone):
        """
            get verify code by id
        :param id:
        :return:
        """
        return self._redis.get(phone)


# sms verify code object
sms = _SmsVerify(redis.vsms)
