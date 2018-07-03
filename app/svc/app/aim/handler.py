"""
    base handler
"""
import tornado.web
from lib.util import mysql
from app.aim import config


class Handler(tornado.web.RequestHandler):
    """
        base handler for request handlers
    """
    def initialize(self):
        """
            pass
        :return:
        """
        # init database
        self.db = mysql.DBMysql(config.mysql)

    def prepare(self):
        """
            pass
        :return:
        """
        pass

    def on_finish(self):
        """

        :return:
        """
        # close database
        self.db.close()
