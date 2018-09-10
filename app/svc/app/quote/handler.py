"""
    base handler
"""
import tornado.web
from app.quote import config


class Handler(tornado.web.RequestHandler):
    """
        base handler for request handlers
    """
    def initialize(self):
        """
            overwrite: initialize
        :return:
        """
        pass

    def set_default_headers(self):
        """
            overwrite: set default headers
        :return:
        """
        for header in config.HEADERS:
            self.set_header(*header)

    @property
    def arguments(self):
        args = {}
        for arg in self.request.arguments.keys():
            args[arg] = self.get_argument(arg)
        return args
