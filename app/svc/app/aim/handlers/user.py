"""
    user handlers
"""
from tlib import validator, hash
from .. import access, handler, daos, error, protocol, verify, forms


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
        form = forms.user.UserExist(**self.arguments)

        # check if user has exist
        userdao = daos.user.UserDao(self.db)

        if len(userdao.get(phone=form.phone)) > 0:
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
        form = forms.user.UserRegister(**self.arguments)

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


class LoginHandler(handler.Handler):
    @access.exptproc
    def post(self):
        """
            login
        :return:
        """
        # get parameters
        form = forms.user.UserLogin(**self.arguments)

        # init user model
        userdao = daos.user.UserDao(self.db)

        # get user from database
        user = userdao.get(user=form.user)

        ## check user ##
        # user not exist or password invalid
        if user is None or hash.sha1(form.pwd) != user.pwd:
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
    @access.exptproc
    @access.needlogin
    def post(self):
        """
            echo
        :return:
        """
        # get arguments
        form = forms.user.UserChangePwd(**self.arguments)

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


class ResetPwdHandler(handler.Handler):
    @access.exptproc
    def post(self):
        """
            echo
        :return:
        """
        # get arguments
        form = forms.user.UserResetPwd(**self.arguments)

        # check verify code
        if verify.sms.get(form.phone) != form.vcode:
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
        data = []
        for bank in banks:
            data.append({'id':bank.get('id'),
                         'name': bank.get('name'),
                         'idc': bank.get('idc'),
                         'bank': bank.get('bank'),
                         'account': bank.get('account'),
                         'ctime': bank.get('ctime'),
                         'mtime': bank.get('mtime'),
                         'user': bank.get('user_id')})

        self.write(protocol.success(data=data))


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
        data = []
        for coupon in coupons:
            data.append({'id':coupon.get('id'),
                         'name': coupon.get('name'),
                         'money': coupon.get('money'),
                         'status': coupon.get('status'),
                         'ctime': coupon.get('ctime'),
                         'etime': coupon.get('etime'),
                         'utime': coupon.get('utime'),
                         'user': coupon.get('user_id')})

        self.write(protocol.success(data=data))


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

        # response data
        data = []
        for bill in bills:
            data.append({'id':bill.get('id'),
                         'code': bill.get('code'),
                         'item': bill.get('item'),
                         'detail': bill.get('detail'),
                         'bmoney': bill.get('bmoney'),
                         'lmoney': bill.get('lmoney'),
                         'ctime': bill.get('ctime'),
                         'user': bill.get('user_id')})

        self.write(protocol.success(data=data))


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
        data = []
        for charge in charges:
            data.append({'id': charge.get('id'),
                         'code': charge.get('code'),
                         'money': charge.get('money'),
                         'status': charge.get('status'),
                         'ctime': charge.get('ctime'),
                         'user': charge.get('user_id')})

        self.write(protocol.success(data=data))


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
        data = []
        for draw in draws:
            data.append({'id': draw.get('id'),
                         'code': draw.get('code'),
                         'money': draw.get('money'),
                         'name': draw.get('name'),
                         'idc': draw.get('idc'),
                         'bank': draw.get('bank'),
                         'account': draw.get('account'),
                         'status': draw.get('status'),
                         'ctime': draw.get('ctime'),
                         'user': draw.get('user_id')})

        self.write(protocol.success(data=data))


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
        data = []
        for stock in stocks:
            data.append({'id': stock.get('id'),
                         'code': stock.get('code'),
                         'name': stock.get('name'),
                         'ctime': stock.get('ctime'),
                         'user': stock.get('user')})

        self.write(protocol.success(data=data))