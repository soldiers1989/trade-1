"""
    stock quote service
"""
from sec.util import table
from sec.stock.quote import quote
from sec.stock.quote.tdx import agent


class TdxQuote(quote.Quote):
    def __init__(self, host, port, servers, timeout=5):
        """
            init tdx quote service
        :param host: str, remote agent host
        :param port: str, remote agent port
        :param servers: array, quote server list, [(ip, port), (ip, port), ...]
        :param timeout: int, connection timeout in seconds
        """
        self._agent = agent.Agent(host, port, servers, timeout)

    def get(self, code):
        """
            get quote of stock
        :param code: str, stock code
        :return:
        """
        try:
            self.monitor.add_total()
            result = self._agent.get(code)
            self.monitor.add_succeed()
            self.monitor.clear_failures()
            return result
        except Exception as e:
            self.monitor.add_failed()
            self.monitor.add_failure(str(e))
            return None

    def gets(self, codes):
        """
            get quote of stocks
        :param codes:
        :return:
        """
        try:
            self.monitor.add_total()
            result = self._agent.gets(codes)
            self.monitor.add_succeed()
            self.monitor.clear_failures()
            return result
        except Exception as e:
            self.monitor.add_failed()
            self.monitor.add_failure(str(e))
            return None


if __name__ == "__main__":
    q = TdxQuote("172.16.21.135", 8080)

    res = q.connect("175.6.5.153", 7709)
    print(res)

    res = q.query_count(0)
    print(res)

    res = q.query_gphq(0, "000725")
    print(res)