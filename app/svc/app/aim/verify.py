"""
    sms manager
"""
from app.aim import redis


# redis item
class _RedisItem:
    def __init__(self, name, expires):
        self.name = name
        self.expires = expires


# redis for sms
_smsredis = redis.aim

# sms name for redis
def _smsid(phone, name):
    """
        generate sms key by phone & name
    :param phone:
    :param name:
    :return:
    """
    return 'sms_' + phone + "_" + name

# vode verify using sms
class _Sms:
    @staticmethod
    def set(phone, name, val, expires):
        """
            set message
        :param name:
        :param val:
        :param expires:
        :return:
        """
        key = _smsid(phone, name)
        _smsredis.setex(key, val, expires)

    @staticmethod
    def get(phone, name, default=None):
        """
            get message
        :param name:
        :param default:
        :return:
        """
        key = _smsid(phone, name)
        val = _smsredis.get(key)
        return val if val is not None else default

    @staticmethod
    def delete(phone, name):
        """
            delete message
        :param name:
        :return:
        """
        key = _smsid(phone, name)
        _smsredis.delete(key)

    # sms verify code definition
    register = _RedisItem('register', 120)

sms = _Sms


# image redis
_imgredis = redis.aim


# image name for redis
def _imgid(sid, name):
    """
        generate external key by sid and name
    :param sid: session id
    :param name: usage name
    :return:
    """
    return 'img_' + sid + "_" + name


# vode verify using image
class _Image:
    @staticmethod
    def set(sid, name, val, expires):
        """
            set message
        :param name:
        :param val:
        :param expires:
        :return:
        """
        key = _imgid(sid, name)
        _smsredis.setex(key, val, expires)

    @staticmethod
    def get(sid, name, default=None):
        """
            get message
        :param name:
        :param default:
        :return:
        """
        key = _imgid(sid, name)
        val = _smsredis.get(key)
        return val if val is not None else default

    @staticmethod
    def delete(sid, name):
        """
            delete message
        :param name:
        :return:
        """
        key = _imgid(sid, name)
        _smsredis.delete(key)

    # image verify code items defination
    register = _RedisItem('register', 120)

img = _Image