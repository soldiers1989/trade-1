"""
    east money quote data
"""
import time
from lib.stock.util import stock
from lib.stock.quote import quote, server, error
from lib.stock.quote.emoney import config, parser, path


class EmoneyQuote(quote.Quote):
    def __init__(self, hosts=config.HOSTS, timeout=config.TIMEOUT, maxfailed=config.MAXFAILED):
        """
            init sina quote
        :param hosts: array, server hosts
        :param maxfailed:
        """
        # servers
        servers = server.Servers(hosts, timeout, maxfailed)

        # init super
        super(EmoneyQuote, self).__init__(config.ID, config.NAME, servers)

    def test(self, code):
        """
            try to get quote from specified host(may disabled), if succeed the host will be enabled,
            used to restart a disabled agent host
        :param code: str, stock code
        :param host: str, host in agent
        :return:
        """
        # add header referer
        headers = self.headers(code)
        # make path
        urlpath = path.make(code)

        return self.servers.test(urlpath, headers)

    def get(self, code):
        """
            request quote of stock @code from sina quote url
        :param code: str, stock code
        :param retry: int, retry number if failed
        :return:
        """
        try:
            stime = time.time()
            # make header
            headers = self.headers(code)

            # make path
            urlpath = path.make(code)
            # request remote service
            resp = self.servers.get(urlpath, headers, config.RETRY)
            # parse result
            results = parser.parse(resp)
            etime = time.time()

            self.addsucceed(etime - stime)

            # results
            return results
        except error.NoneServerError as e:
            self.disable()
            self.addfailed(str(e))
            raise e
        except Exception as e:
            self.addfailed(str(e))
            raise e

    def gets(self, codes):
        """
            get quote of stocks
        :param codes: array, stock codes array
        :param retry: int, retry number if failed
        :return:
        """
        results = []
        for code in codes:
            results.append(self.get(code))
        return results

    def headers(self, code):
        """
            make request headers
        :param code:
        :return:
        """
        headers = config.HEADERS
        headers.update({"Referer": "http://quote.eastmoney.com/" + stock.addse(code) + ".html"})
        return headers
