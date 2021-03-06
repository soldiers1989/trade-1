"""
    securities account for trade
"""
from .. import account, error
from .... import rpc


class Account(account.Account):
    def __init__(self, **kwargs):
        """
            init account
        :param account: str, 登录账户，一般为资金账户或者客户好
        :param pwd: str, 登录密码
        :param money: str, 账户资金余额
        """
        # get args
        self._account, self._pwd, self._server = kwargs.get('account'), kwargs.get('pwd'), kwargs.get('server')

        # check args
        if self._account is None or self._pwd is None or self._server is None:
            raise error.TradeError('missing account parameters')

        baseurl, token, safety = self._server['baseurl'], self._server['token'], self._server['safety']

        # remote rpc
        self._rpc = rpc.Broker(baseurl, token, safety)

    def login(self):
        """
            账户登录
        :return: dict
            {'status': status, 'msg': msg, 'data':{}}
        """
        return self._rpc.login(account=self._account, pwd=self._pwd)

    def logout(self):
        """
            账户退出
        :return:
            (True|False, result message string)
        """
        return self._rpc.logout(account=self._account)

    def status(self):
        """
            get account status
        :return:
        """
        data = {
            'account': self._account,
            'pwd': self._pwd,
            'server': self._server,
        }
        return data

    def quote(self, zqdm):
        """
            查询股票实时行情
        :param zqdm: str, stock code
        :return:
            dict
        """
        raise error.TradeError('quote not supported')

    def query(self, type, sdate=None, edate=None):
        """
            查询账户当前或者历史数据
        :param type: str, data type: dqzc/dqcc/drwt/drcj/kcwt/gdxx/lswt/lscj/jgd
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
            list/dict
        """
        return self._rpc.query(account=self._account, type=type, sdate=sdate, edate=edate)

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
        return self._rpc.place(account=self._account, symbol=zqdm, otype=otype, ptype=ptype, oprice=price, ocount=count)

    def cancel(self, zqdm, orderno):
        """
            委托撤单
        :param zqdm: str, stock code
        :param orderno: str, order number
        :return:
        """
        return self._rpc.cancel(account=self._account, ocount=orderno)

# register channel
account.register('mock', Account)
