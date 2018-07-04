"""
    access protection
"""
import tornado.web
from app.aim import error, config, protocol, log


def needlogin(handler_func):
    """
        handler access protection
    :param handler_func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        uid = self.get_argument('uid')
        if uid != self.session.get('uid'):
            self.write(protocol.failed('not login, access denied'))
        else:
            return handler_func(self, *args, **kwargs)
    return wrapper


def needtoken(handler_func):
    """
        handler access protection
    :param handler_func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        token = self.get_argument('token')
        if token != config.ACCESS_TOKEN:
            self.write(protocol.failed('invalid token, access denied'))
        else:
            return handler_func(self, *args, **kwargs)

    return wrapper


def exptproc(handler_func):
    def wrapper(self, *args, **kwargs):
        try:
            return handler_func(self, *args, **kwargs)
        except tornado.web.MissingArgumentError as e:
            self.write(protocol.failed(**error.MISSING_PARAMETERS))
            log.error(str(e))
        except Exception as e:
            self.write(protocol.failed(**error.SERVER_EXCEPTION))
            log.error(str(e))
    return  wrapper
