import json
from .. import access, handler, trader, protocol, alias, forms


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
        account = json.loads(self.request.body.decode())
        trader.default.add(account['id'], **account)
        self.write(protocol.success())


class DelAccount(handler.Handler):
    """
        delete account
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            delete account
        :return:
        """
        form = forms.account.Delete(**self.arguments)
        resp = trader.default.delete(form.aid)
        self.write(resp)


class ClearAccount(handler.Handler):
    """
        clear all account
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            clear all account
        :return:
        """
        resp = trader.default.clear()
        self.write(resp)


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
        try:
            aid = self.get_argument('account', None)
            resp = trader.default.login(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


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
        try:
            aid = self.get_argument('account', None)
            resp = trader.default.logout(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


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
        try:
            aid = self.get_argument('account', None)
            resp = trader.default.status(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryGdxx(handler.Handler):
    """
        query gdxx
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_gdxx(aid)
            self.write(protocol.upgrade(resp, alias.gdxx))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryDqzc(handler.Handler):
    """
        query dqzc
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_dqzc(aid)
            self.write(protocol.upgrade(resp, alias.dqzc))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryDqcc(handler.Handler):
    """
        query dqzc
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_dqcc(aid)
            self.write(protocol.upgrade(resp, alias.dqcc))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryDrwt(handler.Handler):
    """
        query drwt
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_drwt(aid)
            self.write(protocol.upgrade(resp, alias.drwt))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryDrcj(handler.Handler):
    """
        query drcj
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_drcj(aid)
            self.write(protocol.upgrade(resp, alias.drcj))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryKcwt(handler.Handler):
    """
        query kcwt
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_kcwt(aid)
            self.write(protocol.upgrade(resp, alias.kcwt))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryLswt(handler.Handler):
    """
        query lswt
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, sdate, edate = self.get_argument('account'), self.get_argument('sdate'), self.get_argument('edate')
            resp = trader.default.query_lswt(aid, sdate, edate)
            self.write(protocol.upgrade(resp, alias.lswt))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryLscj(handler.Handler):
    """
        query lscj
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, sdate, edate = self.get_argument('account'), self.get_argument('sdate'), self.get_argument('edate')
            resp = trader.default.query_lscj(aid, sdate, edate)
            self.write(protocol.upgrade(resp, alias.lscj))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryJgd(handler.Handler):
    """
        query jgd
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, sdate, edate = self.get_argument('account'), self.get_argument('sdate'), self.get_argument('edate')
            resp = trader.default.query_jgd(aid, sdate, edate)
            self.write(protocol.upgrade(resp, alias.jgd))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryGphq(handler.Handler):
    """
        query gphq
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, code = self.get_argument('account'), self.get_argument('code')
            resp = trader.default.query_gphq(aid, code)
            self.write(protocol.upgrade(resp, alias.gphq))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderXjmr(handler.Handler):
    """
        order xjmr
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, gddm, code, price, count = self.get_argument('account'), self.get_argument('gddm'), self.get_argument('code'), self.get_argument('price'), self.get_argument('count')
            resp = trader.default.order_xjmr(aid, gddm, code, price, count)
            self.write(protocol.upgrade(resp, alias.xjmr))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderXjmc(handler.Handler):
    """
        order xjmc
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, gddm, code, price, count = self.get_argument('account'), self.get_argument('gddm'), self.get_argument('code'), self.get_argument('price'), self.get_argument('count')
            resp = trader.default.order_xjmc(aid, gddm, code, price, count)
            self.write(protocol.upgrade(resp, alias.xjmc))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderSjmr(handler.Handler):
    """
        order sjmr
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, gddm, code, price, count = self.get_argument('account'), self.get_argument('gddm'), self.get_argument('code'), self.get_argument('price'), self.get_argument('count')
            resp = trader.default.order_sjmr(aid, gddm, code, price, count)
            self.write(protocol.upgrade(resp, alias.sjmr))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderSjmc(handler.Handler):
    """
        order sjmc
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, gddm, code, price, count = self.get_argument('account'), self.get_argument('gddm'), self.get_argument('code'), self.get_argument('price'), self.get_argument('count')
            resp = trader.default.order_sjmc(aid, gddm, code, price, count)
            self.write(protocol.upgrade(resp, alias.sjmc))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderCancel(handler.Handler):
    """
        order cancel
    """

    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, seid, orderno = self.get_argument('account'), self.get_argument('seid'), self.get_argument('orderno')
            resp = trader.default.cancel_order(aid, seid, orderno)
            self.write(protocol.upgrade(resp, alias.wtcd))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))
