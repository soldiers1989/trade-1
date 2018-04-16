"""
    trade agent base class, all agent must be inherit from this class
"""


class Agent:
    def __init__(self):
        pass

    def login(self, account, pwd, ip, port, dept, version):
        """
            账户登录
        :param account:
        :param pwd:
        :param ip:
        :param port:
        :param dept:
        :param version:
        :return:
            (True|False, result message string)
        """
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

    def query_gphq(self, account, code, market="0"):
        """
            查询股票行情
        :param account: str, in, user account
        :param code: str, in, stock code
        :param market: 0 - shenzhen, 1 -shanghai, useless...
        :return:
        """
        pass

    def order_xjmr(self, account, gddm, zqdm, price, count):
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

    def order_xjmc(self, account, gddm, zqdm, price, count):
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

    def order_sjmr(self, account, gddm, zqdm, price, count):
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

    def order_sjmc(self, account, gddm, zqdm, price, count):
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

    def cancel_order(self, account, orderno, market):
        """
            委托撤单
        :param account:
        :param orderno:
        :param market: 0 - shenzhen， 1 - 上海
        :return:
        """
        pass

    def logout(self, account):
        """
            账户退出
        :param account:
        :return:
            (True|False, result message string)
        """
        pass