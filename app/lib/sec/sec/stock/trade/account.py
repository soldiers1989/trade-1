"""
    securities account base class for trade
"""


class Account:
    def __init__(self):
        pass

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

    def order_xjmr(self, zqdm, price, count):
        """
            限价买入
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_xjmc(self, zqdm, price, count):
        """
            限价卖出
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_sjmr(self, zqdm, price, count):
        """
            市价买入
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def order_sjmc(self, zqdm, price, count):
        """
            市价卖出
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def cancel_order(self, orderno):
        """
            委托撤单
        :param orderno:
        :return:
        """
        pass
