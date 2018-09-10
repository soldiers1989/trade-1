"""
    access protection
"""
from app.trade import protocol, config


def needtoken(handler_func):
    """
        handler access protection
    :param handler_func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        token = self.get_argument(config.TOKEN_NAME)
        if token != config.TOKEN_VALUE:
            self.write(protocol.failed(msg='未授权'))
        else:
            return handler_func(self, *args, **kwargs)

    return wrapper
