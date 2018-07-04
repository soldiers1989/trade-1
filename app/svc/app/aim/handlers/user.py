"""
    user handlers
"""
from lib.cube.util import hash
from app.aim import access, handler, models, error, protocol


class LoginHandler(handler.Handler):
    @access.exptproc
    def post(self):
        """
            login
        :return:
        """
        # get parameters
        user, pwd = self.get_argument('user'), self.get_argument('pwd')

        # init user model
        usermodel = models.user.UserModel(self.db)

        # get user from database
        users = usermodel.get(user)

        ## check user ##
        # user not exist
        if len(users) == 0:
            self.write(protocol.failed(**error.USER_OR_PASSWORD_INVALID))
            return

        # password invalid
        if hash.sha1(pwd) != users[0].get('pwd'):
            self.write(protocol.failed(**error.USER_OR_PASSWORD_INVALID))
            return


        # user has disabled
        if users[0].get('disable'):
            self.write(protocol.failed(**error.USER_DISABLED))
            return

        # get user id
        uid = users[0].get('id')

        # set user session
        self.session.set('uid', uid)

        # login success
        self.write(protocol.success(data={'uid':uid, 'sid': self.session.id}))


class LogoutHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            logout
        :return:
        """
        self.session.clear()

        self.write(protocol.success())


class ChangePwdHandler(handler.Handler):
    @access.needlogin
    def post(self):
        """
            echo
        :return:
        """
        try:
            self.write(protocol.success(data=[]))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class FindPwdHandler(handler.Handler):
    @access.needlogin
    def post(self):
        """
            echo
        :return:
        """
        try:
            self.write(protocol.success(data=[]))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))

