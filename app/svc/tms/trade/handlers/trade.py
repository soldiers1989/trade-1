import json
from .. import access, handler, trader, error, protocol


class AddAccount(handler.Handler):
    """
        add new account
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new account
        :return:
        """
        if self.request.body is None:
            raise error.missing_parameters

        account = json.loads(self.request.body.decode())
        resp = trader.default.add(account['id'], **account)
        self.write(protocol.success(data=resp))


class DelAccount(handler.Handler):
    """
        delete account
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            delete account
        :return:
        """
        account = self.get_argument('account')
        resp = trader.default.delete(account)
        self.write(protocol.success(data=resp))


class ClearAccount(handler.Handler):
    """
        clear all account
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            clear all account
        :return:
        """
        resp = trader.default.clear()
        self.write(protocol.success(data=resp))


class LoginAccount(handler.Handler):
    """
        login
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            login
        :return:
        """
        aid = self.get_argument('account', None)
        resp = trader.default.login(aid)
        self.write(protocol.success(data=resp))


class LogoutAccount(handler.Handler):
    """
        login
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            login
        :return:
        """
        aid = self.get_argument('account', None)
        resp = trader.default.logout(aid)
        self.write(protocol.success(data=resp))


class StatusAccount(handler.Handler):
    """
        handler for query account status
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote
        :return:
        """
        aid = self.get_argument('account', None)
        resp = trader.default.status(aid)
        self.write(protocol.success(data=resp))


class Quote(handler.Handler):
    """
        query current stock quote
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        aid, zqdm = self.get_argument('account'), self.get_argument('zqdm')
        resp = trader.default.quote(aid, zqdm)
        self.write(protocol.success(data=resp))


class Query(handler.Handler):
    """
        query current or history data
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote
        :return:
        """
        aid, type, sdate, edate = self.get_argument('account'), self.get_argument('type'), self.get_argument('sdate', None), self.get_argument('edate', None)
        resp = trader.default.query(aid, type, sdate, edate)
        self.write(protocol.success(data=resp))


class Place(handler.Handler):
    """
        place order
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        aid, otype, ptype, zqdm, price, count = self.get_argument('account'), self.get_argument('otype'), self.get_argument('ptype'), self.get_argument('zqdm'), self.get_argument('price'), self.get_argument('count')
        resp = trader.default.place(aid, otype, ptype, zqdm, price, count)
        self.write(protocol.success(data=resp))


class Cancel(handler.Handler):
    """
        cancel order
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        aid, zqdm, orderno = self.get_argument('account'), self.get_argument('zqdm'), self.get_argument('orderno')
        resp = trader.default.cancel(aid, zqdm, orderno)
        self.write(protocol.success(data=resp))
