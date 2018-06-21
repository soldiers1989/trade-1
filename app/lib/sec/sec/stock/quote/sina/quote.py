"""
    quote data from sina
"""
from sec.stock.quote import quote
from sec.stock.quote.sina import agent


class SinaQuote(quote.Quote):
    def __init__(self, hosts=[], timeout=1, kickout=3):
        """
            init with http request timeout
        :param hosts: array, sina quote server hosts
        :param timeout: int, host connection timeout in seconds
        :param kickout: int, host failed kickout in count
        """
        # init agent
        self._agent = agent.Agent(hosts, timeout, kickout)

        # init super
        super(SinaQuote, self).__init__()

    def get(self, code, retry=1):
        """
            get quote of stock
        :param code: str, stock code
        :return:
        """
        try:
            self.monitor.add_total()
            result = self._agent.get(code, retry)
            self.monitor.add_succeed()
            self.monitor.clear_failures()
            return result
        except Exception as e:
            self.monitor.add_failed()
            self.monitor.add_failure(str(e))
            return None

    def gets(self, codes, retry=1):
        """
            get quote of stocks
        :param codes:
        :return:
        """
        try:
            self.monitor.add_total()
            result = self._agent.gets(codes, retry)
            self.monitor.add_succeed()
            self.monitor.clear_failures()
            return result
        except Exception as e:
            self.monitor.add_failed()
            self.monitor.add_failure(str(e))
            return None

    def hosts(self):
        return self._agent.hosts()