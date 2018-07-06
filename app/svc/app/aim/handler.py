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
        # get session id from cookie
        csid = self.get_secure_cookie(config.SESSION_NAME)
        if csid is not None:
            csid = csid.decode()

        # cookie has no session id, try it in the argument
        if csid is None:
            sid = self.get_argument(config.SESSION_NAME, None)
            # get session
            self.session = session.get(sid)

            # set cookie with new session id
            self.set_secure_cookie(config.SESSION_NAME, self.session.id, config.SESSION_COOKIE_TIMEOUT)
        else:
            # get session
            self.session = session.get(csid)

            # check session id
            if self.session.id != csid:
                # set cookie with new session id
                self.set_secure_cookie(config.SESSION_NAME, self.session.id, config.SESSION_COOKIE_TIMEOUT)

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

        # update session expire time if current user is login
        if self.current_user is not None:
            self.session.expire(config.SESSION_TIMEOUT)
