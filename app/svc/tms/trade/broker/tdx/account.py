"""
    securities account for trade
"""
from . import trader, protocol
from .. import account, error


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

    def _decode(self, resp):
        """
            decode protocol
        :param resp:
        :return:
        """
        if resp.get('status') != 0:
            raise error.TradeError(resp.get('msg'))

        return resp.get('data')

    def login(self):
        """
            账户登录
        :return: dict
            {'status': status, 'msg': msg, 'data':{}}
        """
        return self._decode(self._traders.login())

    def logout(self):
        """
            账户退出
        :return:
            (True|False, result message string)
        """
        return self._decode(self._traders.logout())

    def status(self):
        """
            get account status
        :return:
        """
        data = self._account.status()
        data['traders'] = self._traders.status()
        return data

    def quote(self, zqdm):
        """
            查询股票实时行情
        :param zqdm: str, stock code
        :return:
            dict
        """
        # send query
        return self._decode(self._traders.quote(zqdm))

    def query(self, type, sdate=None, edate=None):
        """
            查询账户当前或者历史数据
        :param type: str, data type: dqzc/dqcc/drwt/drcj/kcwt/gdxx/lswt/lscj/jgd
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
            list/dict
        """
        return self._decode(self._traders.query(type, sdate, edate))

    def place(self, otype, ptype, zqdm, price, count):
        """
            委托下单
        :param otype: order type: buy/sell
        :param ptype: price type: xj/sj
        :param zqdm: stock code
        :param price: order price
        :param count: order count
        :return:
        """
        return self._decode(self._traders.place(otype, ptype, zqdm, price, count))

    def cancel(self, zqdm, orderno):
        """
            委托撤单
        :param zqdm: str, stock code
        :param orderno: str, order number
        :return:
        """
        # cancel order
        return self._decode(self._traders.cancel(zqdm, orderno))

# register channel
account.register('tdx', Account)
