"""
    user handlers
"""
from lib.cube.util import hash
from app.aim import access, handler, models, error, protocol, verify, config
from app.util import verifier, validator


class GetSIDHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get session id
        :return:
        """
        sid = self.session.id
        self.write(protocol.success(data={'sid':sid}))


class RegisterHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            user register
        :return:
        """
        # get arguments
        phone, vcode = self.get_argument('phone', None), self.get_argument('vcode', None)

        # get verify image
        if vcode is None:
            chars, imgdata = verifier.image.num(4, 120, 50)

            # save verify chars
            verify.img.set(self.session.id, verify.img.register.name, chars, verify.img.register.expires)

            # response data
            self.set_header('Content-Type', 'image/png')
            self.write(imgdata)

            return

        # sms need phone number
        if phone is None:
            self.write(error.invalid_parameters.data)
            return


        # check phone number
        if not validator.phone(phone):
            self.write(error.invalid_phone.data)
            return

        # check verify code
        svcode = self.session.getext(self.session.ext.VCODE_IMG_REG)
        if svcode is None or vcode.lower() != svcode.lower():
            self.write(error.invalid_access.data)
            return


        # send and save sms
        smscode = verifier.rand.num(4)
        verifier.sms.send(phone, smscode)
        verify.sms.set(phone, verify.sms.register.name, smscode, verify.sms.register.expires)

        # sms has send success
        self.write(protocol.success())


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
            self.write(error.invalid_parameters.data)
            return

        # check verify code
        if vcode.lower() != sms.get(phone, sms.REGISTER).lower():
            self.write(error.wrong_sms_verify_code.data)
            return

        # init user model
        usermodel = models.user.UserModel(self.db)

        # check exists user
        if len(usermodel.get(phone)) > 0:
            self.write(error.user_exists.data)
            return

        # create user
        if usermodel.add(phone, hash.sha1(pwd)) != 1:
            self.write(error.user_register.data)
            return

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

