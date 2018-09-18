from tlib import token
from . import config


def make(params):
    """
        add token to params
    :param params:
    :return:
    """
    if not config.ENABLE_KEY:
        return params

    return token.generate(params, config.PRIVATE_KEY)