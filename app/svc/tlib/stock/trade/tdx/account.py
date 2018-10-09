"""
    securities account for trade
"""
from .. import account, error
from . import trader, protocol, util


class Account(account.Account):
    def __init__(self, **kwargs):
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
        # get args
        acnt, pwd = kwargs.get('account'), kwargs.get('pwd')
        laccount, lpwd, taccount, tpwd = kwargs.get('laccount', acnt), kwargs.get('lpwd', pwd), kwargs.get('taccount', acnt), kwargs.get('tpwd', pwd)
        dept, version, gddm, agents, servers = kwargs.get('dept'), kwargs.get('version'), kwargs.get('gddm'), kwargs.get('agents'), kwargs.get('servers')

        # check args
        if laccount is None or lpwd is None or taccount is None or tpwd is None or dept is None or version is None or gddm is None or agents is None or servers is None:
            raise error.TradeError('missing account parameters')

        # init account & traders
        self._account = trader.Account(laccount, lpwd, taccount, tpwd, dept, version, gddm)
        self._traders = trader.Traders(self._account, agents, servers)

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

    def query_gphq(self, zqdm):
        """
            查询股票行情
        :param zqdm: str, in, stock code
        :return:
        """
        try:
            # send query
            return self._traders.quote(zqdm)
        except Exception as e:
            return protocol.failed(str(e))

    def order_xjmr(self, zqdm, price, count):
        """
            限价买入
        :param zqdm: str, in, 证券代码
        :param price: float, in, 委托价格
        :param count: int, in, 委托数量，100整数倍
        :return:
        """
        try:
            # send order to remote
            return self._traders.order(protocol.query.buy, protocol.query.xj, zqdm, price, count)
        except Exception as e:
            return protocol.failed(str(e))

    def order_xjmc(self, zqdm, price, count):
        """
            限价卖出
        :param zqdm: str, in, 证券代码
        :param price: float, in, 委托价格
        :param count: int, in, 委托数量，100整数倍
        :return:
        """
        try:
            # send order to remote
            return self._traders.order(protocol.query.sell, protocol.query.xj, zqdm, price, count)
        except Exception as e:
            return protocol.failed(str(e))

    def order_sjmr(self, zqdm, price, count):
        """
            市价买入
        :param zqdm: str, in, 证券代码
        :param price: float, in, 委托价格
        :param count: int, in, 委托数量，100整数倍
        :return:
        """
        try:
            # send order to remote
            return self._traders.order(protocol.query.buy, protocol.query.sj, zqdm, price, count)
        except Exception as e:
            return protocol.failed(str(e))

    def order_sjmc(self, zqdm, price, count):
        """
            市价卖出
        :param zqdm: str, in, 证券代码
        :param price: float, in, 委托价格
        :param count: int, in, 委托数量，100整数倍
        :return:
        """
        try:
            # send order to remote
            return self._traders.order(protocol.query.sell, protocol.query.sj, zqdm, price, count)
        except Exception as e:
            return protocol.failed(str(e))

    def cancel_order(self, zqdm, orderno):
        """
            委托撤单
        :param zqdm: str, in 证券代码
        :param orderno: str, in, 委托编号
        :return:
        """
        try:
            # get se id
            seid = util.getse(zqdm)
            if seid is None:
                return protocol.failed('error securities code')

            # cancel order
            return self._traders.cancel(seid, orderno)
        except Exception as e:
            return protocol.failed(str(e))


# register channel
account.register('tdx', Account)
