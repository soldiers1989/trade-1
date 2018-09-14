"""
    user handlers
"""
from trpc import sms
from tlib import validator, hash, rand
from .. import access, handler, daos, error, protocol, verify, forms, config, msgtpl


class SessionGetHandler(handler.Handler):
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
        form = forms.user.UserExist(**self.arguments)

        # check if user has exist
        userdao = daos.user.UserDao(self.db)

        if len(userdao.get(phone=form.phone)) > 0:
            data = {'exist': True}
        else:
            data = {'exist': False}

        return self.write(protocol.success(data=data))


class UserRegisterHandler(handler.Handler):
    @access.exptproc
    def post(self):
        """
            user register
        :return:
        """
        # get arguments
        form = forms.user.UserReg(**self.arguments)

        # generate password if not set
        if form.pwd is None:
            form.pwd = rand.alnum(8)

        # check arguments
        if not validator.phone(form.phone) and not validator.password(form.pwd):
            raise error.invalid_parameters

        # check verify code
        scode = verify.sms.get(form.phone)
        if scode is None or form.vcode.lower() != scode.lower():
            raise error.wrong_sms_verify_code

        # init user model
        userdao = daos.user.UserDao(self.db)

        # check exists user
        if len(userdao.get(phone=form.phone)) > 0:
            raise error.user_exists

        # create user
        if userdao.add(form.phone, hash.sha1(form.pwd)) != 1:
            raise error.user_register

        # get user
        user = userdao.get(user=form.phone)

        # set user session
        self.session.set('uid', user.id)
        self.session.set('phone', user.phone)

        # login success
        self.write(protocol.success(data={'uid':user.id, 'sid': self.session.id}))


class UserLoginHandler(handler.Handler):
    @access.exptproc
    def post(self):
        """
            login
        :return:
        """
        # get parameters
        form = forms.user.UserLogin(**self.arguments)

        # check parameters
        if form.pwd is None and form.vcode is None:
            raise error.invalid_parameters

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user from database
        user = userdao.get(user=form.user)

        # user not exist
        if user is None: # register
            if form.vcode is None:
                raise error.invalid_parameters

            # check verify code
            scode = verify.sms.get(form.phone)
            if scode is None or form.vcode.lower() != scode.lower():
                raise error.wrong_sms_verify_code

            # generate password if not set
            if form.pwd is None:
                form.pwd = rand.alnum(8)

            # check arguments
            if not validator.phone(form.user) and not validator.password(form.pwd):
                raise error.invalid_parameters

            # init user model
            userdao = daos.user.UserDao(self.db)

            # create user
            userdao.add(form.user, hash.sha1(form.pwd))

            # get user
            user = userdao.get(user=form.user)
        else: # login
            # password invalid
            if form.pwd is not None and hash.sha1(form.pwd) != user.pwd:
                raise error.user_or_pwd_invalid

            # verify code invalid
            vcode = verify.sms.get(form.user)
            if form.vcode and vcode and form.vcode.lower() != vcode.lower():
                raise error.user_or_pwd_invalid

            # user has disabled
            if user.disable:
                raise error.user_disabled

        # get user id
        uid, phone = user.id, user.phone
        # set user session
        self.session.set('uid', uid)
        self.session.set('phone', phone)

        # login success
        self.write(protocol.success(data={'uid':uid, 'sid': self.session.id}))


class UserLogoutHandler(handler.Handler):
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


class UserVerifyHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            send sms
        :return:
        """
        # get login user phone number
        phone = self.session.get('phone')
        if phone is None:
            raise error.user_not_login

        # get arguments
        form = forms.user.UserVerifyGet(**self.arguments)

        # check phone number
        if not validator.phone(phone):
            raise error.invalid_parameters

        # get message template
        tpl = msgtpl.sms.get(form.type)
        if tpl is None:
            raise error.invalid_parameters

        # check verify code length
        if not validator.range(form.length, config.LENGTH_VERIFY_CODE_MIN, config.LENGTH_VERIFY_CODE_MAX):
            raise error.invalid_parameters

        # generate verify code
        code = rand.num(form.length)

        # save verify code
        verify.sms.set(phone, code, config.EXPIRE_VERIFY_CODE)

        # send message by template
        sms.send(phone, tpl.format(code))

        # response data
        data = {
            'expires': config.EXPIRE_VERIFY_CODE
        }

        self.write(protocol.success(data = data))

    @access.exptproc
    def post(self):
        """
            check sms
        :return:
        """
        # get login user phone number
        phone = self.session.get('phone')
        if phone is None:
            raise error.user_not_login

        # get arguments
        form = forms.user.UserVerifyPost(**self.arguments)

        # verify code
        sc = verify.sms.get(phone)
        if sc is None or form.code.lower() != sc.lower():
            raise error.wrong_sms_verify_code

        # response success
        self.write(protocol.success())


class UserPwdChangeHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            echo
        :return:
        """
        # get arguments
        form = forms.user.UserPwdChange(**self.arguments)

        # check new password
        if not validator.password(form.npwd):
            raise error.invalid_parameters

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user from database
        uid = self.get_current_user()
        user = userdao.get(id = uid)[0]

        # match old password
        if hash.sha1(form.opwd) != user.get('pwd'):
            raise error.user_pwd_invalid

        # update password
        userdao.update(uid, pwd=hash.sha1(form.npwd))

        self.write(protocol.success())


class UserPwdResetHandler(handler.Handler):
    @access.exptproc
    def post(self):
        """
            echo
        :return:
        """
        # get arguments
        form = forms.user.UserPwdReset(**self.arguments)

        # check verify code
        sc = verify.sms.get(form.phone)
        if sc is None or sc != form.vcode:
            raise error.wrong_sms_verify_code

        # check user if exist
        userdao = daos.user.UserDao(self.db)
        user = userdao.get(phone=form.phone)
        if not user:
            raise error.invalid_parameters

        # get user id
        uid = user.id

        # check new password
        if not validator.password(form.npwd):
            raise error.invalid_parameters

        # set new password
        userdao.update(uid, pwd=hash.sha1(form.npwd))

        self.write(protocol.success())


class GetBankHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            bank card
        :return:
        """
        # get user id
        uid = self.get_current_user()

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user banks
        banks = userdao.getbank(user_id=uid, deleted=False)

        # response data
        self.write(protocol.success(data=banks))


class AddBankHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            bank card
        :return:
        """
        # get arguments
        name, idc, bank, account = self.get_argument('name'), self.get_argument('idc'), self.get_argument('bank'), self.get_argument('account')

        # get user id
        uid = self.get_current_user()

        # init user model
        userdao = daos.user.UserDao(self.db)

        # add user bank card
        userdao.addbank(uid, name, idc, bank, account)

        self.write(protocol.success())


class DelBankHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            bank card
        :return:
        """
        # get arguments
        id = self.get_argument('id')

        # get user id
        uid = self.get_current_user()

        # init user model
        userdao = daos.user.UserDao(self.db)

        # add user bank card
        userdao.delbank(uid, id)

        self.write(protocol.success())


class GetCouponHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            bank card
        :return:
        """
        # get user id
        uid = self.get_current_user()

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user coupons
        coupons = userdao.getcoupon(uid)

        # response data
        self.write(protocol.success(data=coupons))


class GetBillHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            bills
        :return:
        """
        # get user id
        uid = self.get_current_user()

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user bills
        bills = userdao.getbill(uid)

        self.write(protocol.success(data=bills))


class GetChargeHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            charge record
        :return:
        """
        # get user id
        uid = self.get_current_user()

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user charges
        charges = userdao.getcharge(uid)

        # response data
        self.write(protocol.success(data=charges))


class GetDrawHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            draw record
        :return:
        """
        # get user id
        uid = self.get_current_user()

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user draws
        draws = userdao.getdraw(uid)

        # response data
        self.write(protocol.success(data=draws))


class GetStockHandler(handler.Handler):
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            user stock
        :return:
        """
        # get user id
        uid = self.get_current_user()

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user stocks
        stocks = userdao.getstock(uid)

        # response data
        self.write(protocol.success(data=stocks))