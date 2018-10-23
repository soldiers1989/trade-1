"""
    agent to sina quote data
"""
import time
from .. import quote, server, error
from . import config, parser


class CNInfoQuote(quote.Quote):
    def __init__(self, hosts=config.HOSTS, timeout=config.TIMEOUT, maxfailed=config.MAXFAILED):
        """
            init sina quote
        :param hosts: array, server hosts
        :param maxfailed:
        """
        # servers
        servers = server.Servers(hosts, timeout, maxfailed)

        # init super
        super(CNInfoQuote, self).__init__(config.ID, config.NAME, servers)

    def test(self, date):
        """

        :param date:
        :return:
        """
        # headers
        headers = config.HEADERS

        # make path
        urlpath = config.PATHS[0]

        return self.servers.test(urlpath, headers)

    def fetch(self, date):
        """

        :param date:
        :return:
        """
        try:
            stime = time.time()

            # results
            results = []

            # make header
            headers = config.HEADERS
            # fetch shanghai&shenzhen exchanges data
            for path in config.PATHS:
                # make path
                urlpath = path % date
                # request remote service
                resp = self.servers.get(urlpath, headers, config.RETRY).json()
                # parse result
                results.extend(parser.parse(resp))

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
