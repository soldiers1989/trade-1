"""
    sms manager
"""
from app.aim import redis


# verify code using sms
class _Sms:
    """
        sms verify code cache
    """
    def __init__(self, redis):
        """
            init
        :param redis:
        """
        self._redis = redis

    def _id(self, phone, name):
        """
            generate sms key by phone & name
        :param phone:
        :param name:
        :return:
        """
        return 'sms_' + phone + "_" + name

    def set(self, phone, name, val, expires):
        """
            set message
        :param name:
        :param val:
        :param expires:
        :return:
        """
        key = self._id(phone, name)
        self._redis.setex(key, val, expires)

    def get(self, phone, name, default=None):
        """
            get message
        :param name:
        :param default:
        :return:
        """
        key = self._id(phone, name)
        val = self._redis.get(key)
        return val if val is not None else default

    def delete(self, phone, name):
        """
            delete message
        :param name:
        :return:
        """
        key = self._id(phone, name)
        self._redis.delete(key)


sms = _Sms(redis.aim)


# vode verify using image
class _Image:
    def __init__(self, redis):
        """
            init
        :param redis:
        """
        self._redis = redis

    def _id(self, sid, name):
        """
            generate external key by sid and name
        :param sid: session id
        :param name: usage name
        :return:
        """
        return 'img_' + sid + "_" + name

    def set(self, sid, name, val, expires):
        """
            set message
        :param name:
        :param val:
        :param expires:
        :return:
        """
        key = self._id(sid, name)
        self._redis.setex(key, val, expires)

    def get(self, sid, name, default=None):
        """
            get message
        :param name:
        :param default:
        :return:
        """
        key = self._id(sid, name)
        val = self._redis.get(key)
        return val if val is not None else default

    def delete(self, sid, name):
        """
            delete message
        :param name:
        :return:
        """
        key = self._id(sid, name)
        self._redis.delete(key)

# cache for verify code
img = _Image(redis.aim)
