import tornado.web
from app.trade import trader, protocol


class Login(tornado.web.RequestHandler):
    """
        login
    """
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


class Logout(tornado.web.RequestHandler):
    """
        login
    """
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


class Status(tornado.web.RequestHandler):
    """
        handler for query account status
    """
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


class QueryGdxx(tornado.web.RequestHandler):
    """
        query gdxx
    """
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


class QueryDqzc(tornado.web.RequestHandler):
    """
        query dqzc
    """
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


class QueryDqcc(tornado.web.RequestHandler):
    """
        query dqzc
    """
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


class QueryDrwt(tornado.web.RequestHandler):
    """
        query drwt
    """
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


class QueryDrcj(tornado.web.RequestHandler):
    """
        query drcj
    """
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


class QueryKcwt(tornado.web.RequestHandler):
    """
        query kcwt
    """
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


class QueryLswt(tornado.web.RequestHandler):
    """
        query lswt
    """
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


class QueryLscj(tornado.web.RequestHandler):
    """
        query lscj
    """
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


class QueryJgd(tornado.web.RequestHandler):
    """
        query jgd
    """
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


class QueryGphq(tornado.web.RequestHandler):
    """
        query gphq
    """
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


class OrderXjmr(tornado.web.RequestHandler):
    """
        order xjmr
    """
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


class OrderXjmc(tornado.web.RequestHandler):
    """
        order xjmc
    """
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


class OrderSjmr(tornado.web.RequestHandler):
    """
        order sjmr
    """
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


class OrderSjmc(tornado.web.RequestHandler):
    """
        order sjmc
    """
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


class OrderCancel(tornado.web.RequestHandler):
    """
        order cancel
    """
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
