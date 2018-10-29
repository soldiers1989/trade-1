"""
    base handler
"""
import tornado.web
from . import config, mysql


class Handler(tornado.web.RequestHandler):
    """
        base handler for request handlers
    """
    def initialize(self):
        """
            overwrite: initialize
        :return:
        """
        ## init database ##
        self.db = mysql.get()

    def on_finish(self):
        """
            request finished
        :return:
        """
        ## close database ##
        self.db.close()

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

    @property
    def cleaned_arguments(self):
        args = {}
        for arg in self.request.arguments.keys():
            if not arg.startswith('_'):
                args[arg] = self.get_argument(arg)
        return args
