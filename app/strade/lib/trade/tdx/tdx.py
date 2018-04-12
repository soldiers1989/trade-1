"""
    tdx trade service api wrapper, Agent->Tdx
"""
from lib.utl import table
from lib.trade.agent import Agent
from lib.trade.tdx import error, remote, option


class Tdx(Agent):
    def __init__(self, host, port):
        """
            init tdx trade object with remote http service host and port
        :param host: remote http service host
        :param port: remote http service port
        """
        self._remote = remote.Remote(host, port)

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
        # check parameters
        if not (account and pwd and ip and port and dept and version) :
            return False, error.INVALID_PARAMETERS

        try:
            # remote login
            bres, msg = self._remote.login(account, pwd, ip, port, dept, version)

            # login return with remote response
            return bres, msg
        except Exception as e:
            # login failed with exception
            return False, str(e)

    def query_dqzc(self, account):
        """
            当前资产查询
        :param account: in, account
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query dqzc
            bres, msg, data = self._remote.query1(account, option.dqzc.type)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.dqzc.alias))

            return True, tbl.data

        except Exception as e:
            # query dqzc failed with exception
            return False, str(e)

    def query_dqcc(self, account):
        """
            当前持仓查询
        :param account: in, account
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query dqcc
            bres, msg, data = self._remote.query1(account, option.dqcc.type)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.dqcc.alias))

            return True, tbl.data

        except Exception as e:
            # query dqcc failed with exception
            return False, str(e)

    def query_drwt(self, account):
        """
            当日委托查询
        :param account: in, account
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query drwt
            bres, msg, data = self._remote.query1(account, option.drwt.type)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.drwt.alias))

            return True, tbl.data

        except Exception as e:
            # query drwt failed with exception
            return False, str(e)

    def query_drcj(self, account):
        """
            当日成交查询
        :param account: in, account
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query drcj
            bres, msg, data = self._remote.query1(account, option.drcj.type)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.drcj.alias))

            return True, tbl.data

        except Exception as e:
            # query drcj failed with exception
            return False, str(e)

    def query_kcwt(self, account):
        """
            可撤委托查询
        :param account: in, account
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query kcwt
            bres, msg, data = self._remote.query1(account, option.kcwt.type)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.kcwt.alias))

            return True, tbl.data

        except Exception as e:
            # query kcwt failed with exception
            return False, str(e)

    def query_gdxx(self, account):
        """
            股东信息查询
        :param account: in, account
        :return:
            (True, [gddm list]) or (False, error message)
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query gddm
            bres, msg, data = self._remote.query1(account, option.gdxx.type)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            data = table(table.sub(data, option.gdxx.alias))

            # get gddm list
            gddms = data[option.gdxx.gddm]

            return True, gddms

        except Exception as e:
            # query gddm failed with exception
            return False, str(e)

    def query_lswt(self, account, sdate, edate):
        """
            查询历史委托
        :param account:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query lswt
            bres, msg, data = self._remote.query2(account, option.lswt.type, sdate, edate)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.lswt.alias))

            return True, tbl.data

        except Exception as e:
            # query lswt failed with exception
            return False, str(e)

    def query_lscj(self, account, sdate, edate):
        """
            查询历史成交
        :param account:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query lscj
            bres, msg, data = self._remote.query2(account, option.lscj.type, sdate, edate)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.lscj.alias))

            return True, tbl.data

        except Exception as e:
            # query lscj failed with exception
            return False, str(e)

    def query_jgd(self, account, sdate, edate):
        """
            查询交割单
        :param account:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query jgd
            bres, msg, data = self._remote.query2(account, option.jgd.type, sdate, edate)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.jgd.alias))

            return True, tbl.data

        except Exception as e:
            # query jgd failed with exception
            return False, str(e)

    def query_gphq(self, account, code, market="0"):
        """
            查询股票行情
        :param account: str, in, user account
        :param code: str, in, stock code
        :param market: 0 - shenzhen, 1 -shanghai, useless...
        :return:
        """
        # check parameters
        if not account or not code:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query gphq
            bres, msg, data = self._remote.quote(account, code, market)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.gphq.alias))

            return True, tbl.data

        except Exception as e:
            # query gphq failed with exception
            return False, str(e)


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
        # check parameters
        if not account or not gddm or not zqdm or not price or not count:
            return False, error.INVALID_PARAMETERS

        try:
            # send order to remote
            bres, msg, data = self._remote.order(account, option.xjmr.otype, option.xjmr.ptype, gddm, zqdm, price, count)

            # send order failed
            if not bres:
                return  False, msg

            # format order result
            tbl = table(table.sub(data, option.xjmr.alias))

            return True, tbl.data
        except Exception as e:
            return False, str(e)

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
        # check parameters
        if not account or not gddm or not zqdm or not price or not count:
            return False, error.INVALID_PARAMETERS

        try:
            # send order to remote
            bres, msg, data = self._remote.order(account, option.xjmc.otype, option.xjmc.ptype, gddm, zqdm, price, count)

            # send order failed
            if not bres:
                return  False, msg

            # format order result
            tbl = table(table.sub(data, option.xjmc.alias))

            return True, tbl.data
        except Exception as e:
            return False, str(e)

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
        # check parameters
        if not account or not gddm or not zqdm or not price or not count:
            return False, error.INVALID_PARAMETERS

        try:
            # send order to remote
            bres, msg, data = self._remote.order(account, option.sjmr.otype, option.sjmr.ptype, gddm, zqdm, price, count)

            # send order failed
            if not bres:
                return  False, msg

            # format order result
            tbl = table(table.sub(data, option.sjmr.alias))

            return True, tbl.data
        except Exception as e:
            return False, str(e)

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
        # check parameters
        if not account or not gddm or not zqdm or not price or not count:
            return False, error.INVALID_PARAMETERS

        try:
            # send order to remote
            bres, msg, data = self._remote.order(account, option.sjmc.otype, option.sjmc.ptype, gddm, zqdm, price, count)

            # send order failed
            if not bres:
                return  False, msg

            # format order result
            tbl = table(table.sub(data, option.sjmc.alias))

            return True, tbl.data
        except Exception as e:
            return False, str(e)

    def cancel_order(self, account, orderno, market):
        """
            委托撤单
        :param account:
        :param orderno:
        :param market: 0 - shenzhen， 1 - 上海
        :return:
        """
        # check parameters
        if not account or not orderno or not market:
            return False, error.INVALID_PARAMETERS

        try:
            # cancel order
            bres, msg, data = self._remote.cancel(account, orderno, market)

            # cancel order failed
            if not bres:
                return  False, msg

            # format cancel result
            tbl = table(table.sub(data, option.wtcd.alias))

            return True, tbl.data
        except Exception as e:
            return False, str(e)

    def logout(self, account):
        """
            账户退出
        :param account:
        :return:
            (True|False, result message string)
        """
        #check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            #remote logout
            bres, msg =  self._remote.logout(account)

            return bres, msg
        except Exception as e:
            return False, str(e)


if __name__ == "__main__":
    tdx = Tdx("172.16.21.135", 80)
    res = tdx.query_dqzc("29633865")
    print(res)

    res = tdx.query_dqcc("29633865")
    print(res)

    res = tdx.query_drwt("29633865")
    print(res)

    res = tdx.query_drcj("29633865")
    print(res)

    res = tdx.query_kcwt("29633865")
    print(res)

    res = tdx.query_gdxx("29633865")
    print(res)

    res = tdx.query_gphq("29633865", "000001")
    print(res)

    res = tdx.query_lswt("29633865", "20180411", "20180411")
    print(res)

    res = tdx.query_lscj("29633865", "20180411", "20180411")
    print(res)

    res = tdx.query_jgd("29633865", "20180411", "20180411")
    print(res)
