"""
    quote data from sina
"""
from lib.stock.quote import quote, config, sina
from lib.stock.quote.sina import agent


class SinaQuote(quote.Quote):
    def __init__(self, hosts=[], timeout=config.TIMEOUT, kickout=config.KICKOUT):
        """
            init with http request timeout
        :param hosts: array, sina quote server hosts
        :param timeout: floag or tuple(float, floag), host connection timeout in seconds, or tuple(connect timeout, read timeout)
        :param kickout: int, host failed kickout in count
        """
        # init agent
        agt = agent.Agent(hosts, timeout, kickout)

        # init super
        super(SinaQuote, self).__init__(sina.ID, sina.NAME, agt)
