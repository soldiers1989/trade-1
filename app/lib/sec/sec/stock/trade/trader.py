"""
    base trader class
"""


class Trader:
    def __init__(self):
        pass

    def query_dqzc(self, account):
        """
            当前资产查询
        :param account: in, account
        :return:
        """
        pass

    def query_dqcc(self, account):
        """
            当前持仓查询
        :param account: in, account
        :return:
        """
        pass

    def query_drwt(self, account):
        """
            当日委托查询
        :param account: in, account
        :return:
        """
        pass

    def query_drcj(self, account):
        """
            当日成交查询
        :param account: in, account
        :return:
        """
        pass

    def query_kcwt(self, account):
        """
            可撤委托查询
        :param account: in, account
        :return:
        """
        pass

    def query_gdxx(self, account):
        """
            股东信息查询
        :param account: in, account
        :return:
            (True, [gddm list]) or (False, error message)
        """
        pass

    def query_lswt(self, account, sdate, edate):
        """
            查询历史委托
        :param account:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        pass

    def query_lscj(self, account, sdate, edate):
        """
            查询历史成交
        :param account:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        pass

    def query_jgd(self, account, sdate, edate):
        """
            查询交割单
        :param account:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        pass

    def query_gphq(self, account, code):
        """
            查询股票行情
        :param account: str, in, user account
        :param code: str, in, stock code
        :return:
        """
        pass

    def order_xjmr(self, account, zqdm, price, count):
        """
            限价买入
        :param account:
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_xjmc(self, account, zqdm, price, count):
        """
            限价卖出
        :param account:
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_sjmr(self, account, zqdm, price, count):
        """
            市价买入
        :param account:
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_sjmc(self, account, zqdm, price, count):
        """
            市价卖出
        :param account:
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def cancel_order(self, account, orderno):
        """
            委托撤单
        :param account:
        :param orderno:
        :return:
        """
        pass
