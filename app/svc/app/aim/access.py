"""
    access protection
"""
import tornado.web
from . import error, config, logger


def needlogin(handler_func):
    """
        handler access protection
    :param handler_func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        if self.session.get('uid') is None:
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
        token = self.get_argument(config.TOKEN_NAME)
        if token != config.TOKEN_VALUE:
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
            logger.error(str(e))
        except error.ProcessError as e:
            self.write(e.data)
            logger.error(str(e))
        except Exception as e:
            self.write(error.server_exception.data)
            logger.error(str(e))
    return wrapper
