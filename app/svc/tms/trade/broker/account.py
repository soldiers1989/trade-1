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
            查询账户状态
        :return:
        """
        pass

    def quote(self, zqdm):
        """
            查询股票实时行情
        :param zqdm: str, stock code
        :return:
            dict
        """
        pass

    def query(self, type, sdate=None, edate=None):
        """
            查询账户当前或者历史数据
        :param type: str, data type: dqzc/dqcc/drwt/drcj/kcwt/gdxx/lswt/lscj/jgd
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
            list/dict
        """
        pass

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
        pass

    def cancel(self, zqdm, orderno):
        """
            委托撤单
        :param zqdm: str, stock code
        :param orderno: str, order number
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
