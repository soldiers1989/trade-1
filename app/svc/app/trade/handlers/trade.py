from app.trade import access, handler, trader, protocol, alias
from lib.stock import trade


class AddAccount(handler.Handler):
    """
        add new account
    """
    @access.needtoken
    def get(self):
        """
            add new account
        :return:
        """
        try:
            # (login-account, login-password, trade-account, trade-password, department, version, agent servers, trade servers)
            ('29633865', '456789', '29633865', '456789', '0', '7.16', AGENTS, S_ZXJT)  # 中信建投

            laccount, lpwd, taccount, tpwd,   = self.get_argument('laccount'), self.get_argument('lpwd'), self.get_argument('taccount'), self.get_argument('tpwd')
            dept, version = self.get_argument('dept'), self.get_argument('version')
            sagents, strades = self.get_argument('agents'), self.get_argument('trades')

            agentservers = []
            for a0 in sagents.split('|'):
                agents = []
                for a1 in a0.split(','):
                    agents.append(a1.strip())
                agentservers.append(agents)

            tradeservers = []
            for t0 in strades.split('|'):
                trades = []
                for t1 in t0.split(','):
                    trades.append(t1.strip())
                tradeservers.append(trades)

            acount = trade.tdx.account.Account(laccount, lpwd, taccount, tpwd, dept, version, agentservers, tradeservers)

            resp = trader.default.add(laccount, acount)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class DelAccount(handler.Handler):
    """
        delete account
    """
    @access.needtoken
    def get(self):
        """
            delete account
        :return:
        """
        try:
            aid = self.get_argument('account', None)
            resp = trader.default.delete(aid)
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class ClearAccount(handler.Handler):
    """
        clear all account
    """
    @access.needtoken
    def get(self):
        """
            clear all account
        :return:
        """
        try:
            resp = trader.default.clear()
            self.write(resp)
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class LoginAccount(handler.Handler):
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


class LogoutAccount(handler.Handler):
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


class StatusAccount(handler.Handler):
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
            self.write(protocol.upgrade(resp, alias.gdxx))
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
            self.write(protocol.upgrade(resp, alias.dqzc))
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
            self.write(protocol.upgrade(resp, alias.dqcc))
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
            self.write(protocol.upgrade(resp, alias.drwt))
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
            self.write(protocol.upgrade(resp, alias.drcj))
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
            self.write(protocol.upgrade(resp, alias.kcwt))
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
            self.write(protocol.upgrade(resp, alias.lswt))
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
            self.write(protocol.upgrade(resp, alias.lscj))
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
            self.write(protocol.upgrade(resp, alias.jgd))
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
            self.write(protocol.upgrade(resp, alias.gphq))
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
            self.write(protocol.upgrade(resp, alias.xjmr))
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
            self.write(protocol.upgrade(resp, alias.xjmc))
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
            self.write(protocol.upgrade(resp, alias.sjmr))
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
            self.write(protocol.upgrade(resp, alias.sjmc))
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
            self.write(protocol.upgrade(resp, alias.wtcd))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))
