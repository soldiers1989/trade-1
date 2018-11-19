"""
    short message
"""
from . import remote


# business name for sms service
BUSINESS = 'aam'


# template name
class _Tpl:
    verify = 'verify'


tpl = _Tpl


def send(phone, tpl, **params):
    """
        send sms
    :param phone:
    :param tpl:
    :param params:
    :return:
    """
    remote.sms.send(phone, BUSINESS, tpl, **params)
