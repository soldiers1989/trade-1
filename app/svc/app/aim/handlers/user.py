"""
    user handlers
"""
from lib.cube.util import hash
from app.aim import access, handler, models, error, protocol, verify
from app.util import validator


class GetSIDHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get session id
        :return:
        """
        sid = self.session.id
        self.write(protocol.success(data={'sid':sid}))


class UserExistHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            check if user has exist
        :return:
        """
        # get arguments
        phone = self.get_argument('phone')

        # check if user has exist
        usermodel = models.user.UserModel(self.db)

        if len(usermodel.get(phone)) > 0:
            data = {'exist': True}
        else:
            data = {'exist': False}

        return self.write(protocol.success(data=data))


class RegisterHandler(handler.Handler):
    @access.exptproc
    def post(self):
        """
            user register
        :return:
        """
        # get arguments
        phone, pwd, vcode = self.get_argument('phone'), self.get_argument('pwd'), self.get_argument('vcode')

        # check arguments
        if not validator.phone(phone) and not validator.password(pwd):
            raise error.invalid_parameters

        # check verify code
        scode = verify.sms.get(phone)
        if scode is None or vcode.lower() != scode.lower():
            raise error.wrong_sms_verify_code

        # init user model
        usermodel = models.user.UserModel(self.db)

        # check exists user
        if len(usermodel.get(phone)) > 0:
            raise error.user_exists

        # create user
        if usermodel.add(phone, hash.sha1(pwd)) != 1:
            raise error.user_register

        # register success
        self.write(protocol.success())


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
        # user not exist or password invalid
        if len(users) == 0 or hash.sha1(pwd) != users[0].get('pwd'):
            raise error.user_or_pwd_invalid

        # user has disabled
        if users[0].get('disable'):
            raise error.user_disabled

        # get user id
        uid, phone = users[0].get('id'), users[0].get('phone')

        # set user session
        self.session.set('uid', uid)
        self.session.set('phone', phone)

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
        # clear user session data
        self.session.clear()

        # logout success
        self.write(protocol.success())


class ChangePwdHandler(handler.Handler):
    @access.needlogin
    def post(self):
        """
            echo
        :return:
        """
        try:
            # get arguments
            opwd, npwd = self.get_argument('opwd'), self.get_argument('npwd')

            # check old password

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

