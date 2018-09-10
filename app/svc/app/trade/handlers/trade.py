from app.trade import access, handler, trader, protocol


class Login(handler.Handler):
    """
        login
    """
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


class Logout(handler.Handler):
    """
        login
    """
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


class Status(handler.Handler):
    """
        handler for query account status
    """
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
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_gdxx(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryDqzc(handler.Handler):
    """
        query dqzc
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_dqzc(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryDqcc(handler.Handler):
    """
        query dqzc
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_dqcc(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryDrwt(handler.Handler):
    """
        query drwt
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_drwt(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryDrcj(handler.Handler):
    """
        query drcj
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_drcj(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryKcwt(handler.Handler):
    """
        query kcwt
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid = self.get_argument('account')
            resp = trader.default.query_kcwt(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryLswt(handler.Handler):
    """
        query lswt
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, sdate, edate = self.get_argument('account'), self.get_argument('sdate'), self.get_argument('edate')
            resp = trader.default.query_lswt(aid, sdate, edate)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryLscj(handler.Handler):
    """
        query lscj
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, sdate, edate = self.get_argument('account'), self.get_argument('sdate'), self.get_argument('edate')
            resp = trader.default.query_lscj(aid, sdate, edate)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryJgd(handler.Handler):
    """
        query jgd
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, sdate, edate = self.get_argument('account'), self.get_argument('sdate'), self.get_argument('edate')
            resp = trader.default.query_jgd(aid, sdate, edate)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryGphq(handler.Handler):
    """
        query gphq
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, code = self.get_argument('account'), self.get_argument('code')
            resp = trader.default.query_gphq(aid, code)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderXjmr(handler.Handler):
    """
        order xjmr
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, gddm, code, price, count = self.get_argument('account'), self.get_argument('gddm'), self.get_argument('code'), self.get_argument('price'), self.get_argument('count')
            resp = trader.default.order_xjmr(aid, gddm, code, price, count)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderXjmc(handler.Handler):
    """
        order xjmc
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, gddm, code, price, count = self.get_argument('account'), self.get_argument('gddm'), self.get_argument('code'), self.get_argument('price'), self.get_argument('count')
            resp = trader.default.order_xjmc(aid, gddm, code, price, count)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderSjmr(handler.Handler):
    """
        order sjmr
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, gddm, code, price, count = self.get_argument('account'), self.get_argument('gddm'), self.get_argument('code'), self.get_argument('price'), self.get_argument('count')
            resp = trader.default.order_sjmr(aid, gddm, code, price, count)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderSjmc(handler.Handler):
    """
        order sjmc
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, gddm, code, price, count = self.get_argument('account'), self.get_argument('gddm'), self.get_argument('code'), self.get_argument('price'), self.get_argument('count')
            resp = trader.default.order_sjmc(aid, gddm, code, price, count)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class OrderCancel(handler.Handler):
    """
        order cancel
    """
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        try:
            aid, seid, orderno = self.get_argument('account'), self.get_argument('seid'), self.get_argument('orderno')
            resp = trader.default.cancel_order(aid, seid, orderno)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))
