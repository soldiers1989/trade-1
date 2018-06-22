"""
    quote data from east money
"""
from sec.stock.quote import quote, config, emoney
from sec.stock.quote.emoney import agent


class EmoneyQuote(quote.Quote):
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
        super(EmoneyQuote, self).__init__(emoney.ID, emoney.NAME, agt)
