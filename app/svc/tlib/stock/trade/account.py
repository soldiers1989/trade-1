"""
    securities account base class for trade
"""
from . import error


class Account:
    def login(self):
        """
            账户登录
        :return: dict
            {'status': status, 'msg': msg, 'data':{}}
        """
        pass

    def logout(self):
        """
            账户退出
        :return:
            (True|False, result message string)
        """
        pass

    def status(self):
        """
            get account status
        :return:
        """
        pass

    def query_dqzc(self):
        """
            当前资产查询
        :return:
        """
        pass

    def query_dqcc(self):
        """
            当前持仓查询
        :return:
        """
        pass

    def query_drwt(self):
        """
            当日委托查询
        :return:
        """
        pass

    def query_drcj(self):
        """
            当日成交查询
        :return:
        """
        pass

    def query_kcwt(self):
        """
            可撤委托查询
        :return:
        """
        pass

    def query_gdxx(self):
        """
            股东信息查询
        :return:
            (True, [gddm list]) or (False, error message)
        """
        pass

    def query_lswt(self, sdate, edate):
        """
            查询历史委托
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        pass

    def query_lscj(self, sdate, edate):
        """
            查询历史成交
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        pass

    def query_jgd(self, sdate, edate):
        """
            查询交割单
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        pass

    def query_gphq(self, code):
        """
            查询股票行情
        :param code: str, in, stock code
        :return:
        """
        pass

    def order_xjmr(self, gddm, zqdm, price, count):
        """
            限价买入
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_xjmc(self, gddm, zqdm, price, count):
        """
            限价卖出
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_sjmr(self, gddm, zqdm, price, count):
        """
            市价买入
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_sjmc(self, gddm, zqdm, price, count):
        """
            市价卖出
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def cancel_order(self, seid, orderno):
        """
            委托撤单
        :param seid: 0 - shenzhen， 1 - shanghai, useless
        :param orderno:
        :return:
        """
        pass


# exist channels
_channels = {}


def register(name: str, acountcls):
    """
        register an trade channcel
    :param name:
    :param acountcls:
    :return:
    """
    _channels[name] = acountcls


def create(**kwargs):
    """
        create a trade channel account object
    :param kwargs:
    :return:
    """
    channel = kwargs.get('channel')
    if channel is None:
        raise error.TradeError('missing channel.')

    cls = _channels.get(channel)
    if cls is None:
        raise error.TradeError('channel %s is not exist.' % channel)

    return cls(**kwargs)
