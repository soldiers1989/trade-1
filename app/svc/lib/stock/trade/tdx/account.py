"""
    securities account for trade
"""
from lib.stock.trade import account
from lib.stock.trade.tdx import trader, protocol


class Account(account.Account):
    def __init__(self, laccount, lpwd, taccount, tpwd, dept, version, agentservers, tradeservers):
        """
            init account
        :param laccount: str, 登录账户，一般为资金账户或者客户好
        :param lpwd: str, 登录密码
        :param taccount: str, 交易账户，一般为资金账户
        :param tpwd: str, 交易密码
        :param dept: str, 营业部代码
        :param version: str, 客户端版本号
        :param agentservers: array, 代理服务器地址列表, [(id, host, port), (id, host, port), ...]
        :param tradeservers: array, 券商交易服务器地址列表, [(id, ip, port), (id, ip, port), ...]
        """
        self._account = trader.Account(laccount, lpwd, taccount, tpwd, dept, version)
        self._traders = trader.Traders(self._account, agentservers, tradeservers)

    def login(self):
        """
            账户登录
        :return: dict
            {'status': status, 'msg': msg, 'data':{}}
        """
        try:
            return self._traders.login()
        except Exception as e:
            return protocol.failed(str(e))

    def logout(self):
        """
            账户退出
        :return:
            (True|False, result message string)
        """
        try:
            return self._traders.logout()
        except Exception as e:
            return protocol.failed(str(e))

    def status(self):
        """
            get account status
        :return:
        """
        try:
            data = self._account.status()
            data['traders'] = self._traders.status()
            return protocol.success(data=data)
        except Exception as e:
            return protocol.failed(str(e))

    def query_gdxx(self):
        """
            股东信息查询
        :return:
        """
        try:
            # send query
            return self._traders.queryc(protocol.query.gdxx)
        except Exception as e:
            return protocol.failed(str(e))

    def query_dqzc(self):
        """
            当前资产查询
        :return: tuple
            (True, Data) or (False, Message)
        """
        try:
            # send query
            return self._traders.queryc(protocol.query.dqzc)
        except Exception as e:
            return protocol.failed(str(e))

    def query_dqcc(self):
        """
            当前持仓查询
        :return:
        """
        try:
            # send query
            return self._traders.queryc(protocol.query.dqcc)
        except Exception as e:
            return protocol.failed(str(e))

    def query_drwt(self):
        """
            当日委托查询
        :return:
        """
        try:
            # send query
            return self._traders.queryc(protocol.query.drwt)
        except Exception as e:
            return protocol.failed(str(e))

    def query_drcj(self):
        """
            当日成交查询
        :return:
        """
        try:
            # send query
            return self._traders.queryc(protocol.query.drcj)
        except Exception as e:
            return protocol.failed(str(e))

    def query_kcwt(self):
        """
            可撤委托查询
        :return:
        """
        try:
            # send query
            return self._traders.queryc(protocol.query.kcwt)
        except Exception as e:
            return protocol.failed(str(e))

    def query_lswt(self, sdate, edate):
        """
            查询历史委托
           :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        try:
            # send query
            return self._traders.queryh(protocol.query.lswt, sdate, edate)
        except Exception as e:
            return protocol.failed(str(e))

    def query_lscj(self, sdate, edate):
        """
            查询历史成交
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        try:
            # send query
            return self._traders.queryh(protocol.query.lscj, sdate, edate)
        except Exception as e:
            return protocol.failed(str(e))

    def query_jgd(self, sdate, edate):
        """
            查询交割单
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        try:
            # send query
            return self._traders.queryh(protocol.query.jgd, sdate, edate)
        except Exception as e:
            return protocol.failed(str(e))

    def query_gphq(self, code):
        """
            查询股票行情
        :param code: str, in, stock code
        :return:
        """
        try:
            # send query
            return self._traders.quote(code)
        except Exception as e:
            return protocol.failed(str(e))

    def order_xjmr(self, gddm, zqdm, price, count):
        """
            限价买入
        :param gddm: str, in, 股东代码
        :param zqdm: str, in, 证券代码
        :param price: float, in, 委托价格
        :param count: int, in, 委托数量，100整数倍
        :return:
        """
        try:
            # send order to remote
            return self._traders.order(protocol.query.buy, protocol.query.xj, gddm, zqdm, price, count)
        except Exception as e:
            return protocol.failed(str(e))

    def order_xjmc(self, gddm, zqdm, price, count):
        """
            限价卖出
        :param gddm: str, in, 股东代码
        :param zqdm: str, in, 证券代码
        :param price: float, in, 委托价格
        :param count: int, in, 委托数量，100整数倍
        :return:
        """
        try:
            # send order to remote
            return self._traders.order(protocol.query.sell, protocol.query.xj, gddm, zqdm, price, count)
        except Exception as e:
            return protocol.failed(str(e))

    def order_sjmr(self, gddm, zqdm, price, count):
        """
            市价买入
        :param gddm: str, in, 股东代码
        :param zqdm: str, in, 证券代码
        :param price: float, in, 委托价格
        :param count: int, in, 委托数量，100整数倍
        :return:
        """
        try:
            # send order to remote
            return self._traders.order(protocol.query.buy, protocol.query.sj, gddm, zqdm, price, count)
        except Exception as e:
            return protocol.failed(str(e))

    def order_sjmc(self, gddm, zqdm, price, count):
        """
            市价卖出
        :param gddm: str, in, 股东代码
        :param zqdm: str, in, 证券代码
        :param price: float, in, 委托价格
        :param count: int, in, 委托数量，100整数倍
        :return:
        """
        try:
            # send order to remote
            return self._traders.order(protocol.query.sell, protocol.query.sj, gddm, zqdm, price, count)
        except Exception as e:
            return protocol.failed(str(e))

    def cancel_order(self, seid, orderno):
        """
            委托撤单
        :param seid: 0 - shenzhen， 1 - shanghai, useless
        :param orderno: str, in, 委托编号
        :return:
        """
        try:
            # cancel order
            return self._traders.cancel(seid, orderno)
        except Exception as e:
            return protocol.failed(str(e))
