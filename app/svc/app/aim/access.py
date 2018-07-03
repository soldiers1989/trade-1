"""
    access protection
"""
from app.aim import config, protocol


def protect(handler_func):
    """
        handler access protection
    :param handler_func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        token = self.get_argument('token')
        if token != config.TOKEN:
            self.write(protocol.failed('access denied'))
        else:
            return handler_func(self, *args, **kwargs)
    return wrapper
