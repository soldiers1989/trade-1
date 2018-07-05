"""
    access protection
"""
import tornado.web
from app.aim import error, config, log


def needlogin(handler_func):
    """
        handler access protection
    :param handler_func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        uid = self.get_argument('uid')
        if uid != self.session.get('uid'):
            self.write(error.user_not_login.data)
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
            self.write(error.invalid_access.data)
        else:
            return handler_func(self, *args, **kwargs)

    return wrapper


def exptproc(handler_func):
    def wrapper(self, *args, **kwargs):
        try:
            return handler_func(self, *args, **kwargs)
        except tornado.web.MissingArgumentError as e:
            self.write(error.missing_parameters.data)
            log.error(str(e))
        except Exception as e:
            self.write(error.server_exception.data)
            log.error(str(e))
    return  wrapper
