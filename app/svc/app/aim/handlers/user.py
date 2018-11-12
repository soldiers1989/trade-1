"""
    user handlers
"""
import time, datetime
from tlib import validator, hash, rand
from .. import access, handler, error, protocol, verify, forms, config, msgtpl, remote, models


class SessionGetHandler(handler.Handler):
    @access.exptproc
    async def get(self):
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
        with models.db.create() as d:
            if models.User.filter(d, user=form.phone).has():
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
        form.pwd = form.pwd or rand.alnum(8)

        # check verify code
        scode = verify.sms.get(form.phone)
        if scode is None or form.vcode.lower() != scode.lower():
            raise error.wrong_sms_verify_code

        with models.db.atomic() as d:
            # check exists user
            if models.User.filter(d, phone=form.phone).has():
                raise error.user_exists

            # create user
            user = models.User(user=form.phone, phone=form.phone, pwd=hash.sha1(form.pwd), money=0.0, disable=False, ctime=int(time.time()), ltime=int(time.time())).save(d)

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

        with models.db.atomic() as d:
            # get user from database
            user = models.User.filter(d, user=form.user).one()

            # user not exist
            if user is None: # register
                if form.vcode is None:
                    raise error.invalid_parameters

                # check verify code
                scode = verify.sms.get(form.phone)
                if scode is None or form.vcode.lower() != scode.lower():
                    raise error.wrong_sms_verify_code

                # generate password if not set
                form.pwd = form.pwd or rand.alnum(8)

                # create user
                user = models.User(user=form.phone, phone=form.phone, pwd=hash.sha1(form.pwd), money=0.0, disable=False, ctime=int(time.time()), ltime=int(time.time())).save(d)
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
        remote.sms.send(phone, tpl.format(code))

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

        with models.db.atomic() as d:
            # current user id
            uid = self.get_current_user()
            # get user from database
            user = models.User.filter(d, id=uid).one()

            # match old password
            if hash.sha1(form.opwd) != user.get('pwd'):
                raise error.user_pwd_invalid

            # update password
            models.User.filter(d, id=uid).update(pwd=hash.sha1(form.npwd))

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

        with models.db.atomic() as d:
            # get user
            user = models.User.filter(d, phone=form.phone).one()
            # check user if exist
            if not user:
                raise error.invalid_parameters

            # check new password
            if not validator.password(form.npwd):
                raise error.invalid_parameters

            # set new password
            models.User.filter(d, id=user.id).update(pwd=hash.sha1(form.npwd))

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

        with models.db.create() as d:
            # get user banks
            banks = models.UserBank.filter(d, user_id=uid, deleted=False).all()

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

        with models.db.atomic() as d:
            # add user bank card
            bank = models.UserBank(user_id=uid, name=name, idc=idc, bank=bank, account=account, deleted=False, ctime=int(time.time()), mtime=int(time.time())).save(d)

            self.write(protocol.success(data=bank))


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

        with models.db.atomic() as d:
            models.UserBank.filter(d, id=id, user_id=uid).update(deleted=True)
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

        with models.db.create() as d:
            # today
            today = datetime.date.today()

            # get user coupons
            coupons = models.UserCoupon.filter(d, user_id=uid, status='notused', sdate__le=today, edate__ge=today).all()

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

        with models.db.create() as d:
            # get user bills
            bills = models.UserBill.filter(d, user_id=uid).orderby('ctime').desc().all()

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

        with models.db.create() as d:
            # get user charges
            charges = models.UserCharge.filter(d, user_id=uid).orderby('ctime').desc().all()

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

        with models.db.create() as d:
            # get user draws
            draws = models.UserDraw.filter(d, user_id=uid).orderby('ctime').desc().all()

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

        with models.db.create() as d:
            # sql
            sql = '''
                    select a.id as id, b.id as code, b.name as `name`, a.ctime as ctime, a.user_id as user_id
                    from tb_user_stock a, tb_stock b
                    where a.user_id=%s and a.stock_id = b.id and a.deleted=false
                    order by a.ctime desc
                '''
            # args
            args = (uid,)

            # get user stocks
            stocks = models.model.RawModel.select(d, sql, *args)

            # response data
            self.write(protocol.success(data=stocks))