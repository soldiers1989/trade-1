"""
    base handler
"""
import tornado.web
from app.aim import mysql, config, session


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

        ## init session ##
        self.session = session.get(self.get_argument(config.SESSION_ID, None))

    def get_current_user(self):
        """
            overwrite: get current user
        :return:
        """
        return self.session.get('uid')

    def set_default_headers(self):
        """
            overwrite: set default headers
        :return:
        """
        for header in config.HEADERS:
            self.set_header(*header)

    def prepare(self):
        """
            overwrite: prepare
        :return:
        """
        pass

    def on_finish(self):
        """
            overwrite: on finish
        :return:
        """
        # close database
        self.db.close()
