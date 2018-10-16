"""
    access protection
"""
import logging, tornado.web
from . import error, config, protocol
from tlib import token


def needtoken(handler_func):
    """
        handler access protection
    :param handler_func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        if config.ENABLE_KEY and not token.validate(self.arguments, config.PRIVATE_KEY):
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
            logging.error(str(e))
        except error.ProcessError as e:
            self.write(e.data)
            logging.error(str(e))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))
            logging.error(str(e))
    return wrapper
