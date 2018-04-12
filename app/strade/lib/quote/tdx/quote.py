"""
    stock quote service
"""
from lib.utl import table
from lib.quote.agent import Agent
from lib.quote.tdx import option
from lib.quote.tdx.remote import Remote


class TdxQuote(Agent):
    def __init__(self, host, port):
        """
            init tdx trade object with remote http service host and port
        :param host: remote http service host
        :param port: remote http service port
        """
        self._remote = Remote(host, port)

    def connect(self, ip, port):
        """
            连接行情服务器
        :param ip:
        :param port:
        :return: tuple
            (True|False, Response Message)
        """
        try:
            # remote connect
            bres, msg = self._remote.connect(ip, port)

            # return with remote response
            return bres, msg
        except Exception as e:
            return False, str(e)

    def query_count(self, market):
        """
            查询股票数量
        :param market: str, in, 0 - shenzhen, 1 -shanghai
        :return: tuple
            (True, Data) or (False, Message)
        """
        try:
            # remote query gphq
            bres, msg, data = self._remote.count(market)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.gpsl.alias))

            return True, tbl.data

        except Exception as e:
            # query gphq failed with exception
            return False, str(e)

    def query_list(self, market, start):
        """
            查询股票列表
        :param market: str, in, 0 - shenzhen, 1 -shanghai
        :param start: int, in, list start position form 0
        :return: tuple
            (True, Data) or (False, Message)
        """
        try:
            # remote query
            bres, msg, data = self._remote.list(market, start)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.gplb.alias))

            return True, tbl.data

        except Exception as e:
            return False, str(e)

    def query_gphq(self, market, zqdm):
        """
            查询股票行情
        :param market: str, in, 0 - shenzhen, 1 -shanghai
        :param zqdm: str, in, stock code
        :return: tuple
            (True, Data) or (False, Message)
        """
        try:
            # remote query gphq
            bres, msg, data = self._remote.quote(market, zqdm)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result
            tbl = table(table.sub(data, option.gphq.alias))

            return True, tbl.data

        except Exception as e:
            # query gphq failed with exception
            return False, str(e)

    def disconnect(self):
        """
            断开行情服务器
        :return: tuple
            (True|False, Response Message)
        """
        try:
            # remote disconnect
            bres, msg = self._remote.disconnect()

            # return with remote response
            return bres, msg
        except Exception as e:
            return False, str(e)


if __name__ == "__main__":
    q = TdxQuote("172.16.21.135", 8080)

    res = q.connect("175.6.5.153", 7709)
    print(res)

    res = q.query_count(0)
    print(res)

    res = q.query_gphq(0, "000725")
    print(res)