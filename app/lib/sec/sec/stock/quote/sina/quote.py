"""
    quote data from sina
"""
from sec.stock.quote import quote
from sec.stock.quote.sina import agent


class SinaQuote(quote.Quote):
    def __init__(self, timeout=5):
        """
            init with http request timeout
        :param timeout: int, http connection timeout in seconds
        """
        # init agent
        self._agent = agent.Agent(timeout)

        # init super
        super(SinaQuote, self).__init__()

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
