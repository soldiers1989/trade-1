"""
    message
"""
from . import provider, template

# use provider
default = 'aliyun'

# providers
_providers = {
    'aliyun': provider.aliyun
}

# default message sender
_sender = _providers[default]


class MessageError(Exception):
    pass


def send(phone, business, tpl, **params):
    """
        send message use selected provider
    :param phone:
    :param business:
    :param tpl:
    :param params:
    :return:
    """
    # get sign & provider template code
    sign = template.business[business]['sign']
    code = template.business[business]['tpls'][tpl]['code'][default]

    # send message with provider
    result = _sender.send(phone, sign, code, params)

    # return
    return result
