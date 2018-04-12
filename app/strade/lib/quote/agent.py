"""
    quote agent base class, all quote agent must be inherit from this class
"""


class Agent:
    def __init__(self):
        pass

    def connect(self, ip, port):
        """
            连接行情服务器
        :param ip:
        :param port:
        :return: tuple
            (True|False, Response Message)
        """
        pass

    def query_count(self, market):
        """
            查询股票数量
        :param market: str, in, 0 - shenzhen, 1 -shanghai
        :return: tuple
            (True, Data) or (False, Message)
        """
        pass

    def query_list(self, market, start):
        """
            查询股票列表
        :param market: str, in, 0 - shenzhen, 1 -shanghai
        :param start: int, in, list start position form 0
        :return: tuple
            (True, Data) or (False, Message)
        """
        pass

    def query_gphq(self, market, zqdm):
        """
            查询股票行情
        :param market: str, in, 0 - shenzhen, 1 -shanghai
        :param zqdm: str, in, stock code
        :return: tuple
            (True, Data) or (False, Message)
        """
        pass

    def disconnect(self):
        """
            断开行情服务器
        :return: tuple
            (True|False, Response Message)
        """
        pass