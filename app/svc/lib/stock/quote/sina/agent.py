"""
    agent to sina quote data
"""
import math, decimal, random, requests, time
from lib.stock.util import stock, digit
from lib.stock.quote import host


class Agent:
    # sina quote server host
    HOST = "hq.sinajs.cn"
    # request headers
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "hq.sinajs.cn",
        "Referer": "http://vip.stock.finance.sina.com.cn/mkt/"
    }

    def __init__(self, hosts, timeout, kickout):
        """
            init agent
        :param hosts: array, server hosts
        :param timeout:
        """
        # check hosts
        if Agent.HOST not in hosts:
            hosts.append(Agent.HOST)

        # server list & time
        self._hosts = host.Hosts(hosts, kickout)
        self._timeout = timeout

    def test(self, code, host):
        """
            try to get quote from specified host(may disabled), if succeed the host will be enabled,
            used to restart a disabled agent host
        :param code: str, stock code
        :param host: str, host in agent
        :return:
        """
        # find the host
        host = self._hosts.find(host)
        if host is None:
            return  None

        # make request url
        url = self._makeurl(host.host, [code])

        # request
        resp = requests.get(url, headers=Agent.HEADERS, timeout=self._timeout)

        # parse response
        results = self._parse(resp.text)

        return results[0]

    def get(self, code, retry):
        """
            request quote of stock @code from sina quote url
        :param code: str, stock code
        :param retry: int, retry number if failed
        :return:
        """
        result = []

        results = self.gets([code], retry)
        if results is not None and len(results) > 0:
            result = results[0]

        return result

    def gets(self, codes, retry):
        """
            get quote of stocks
        :param codes: array, stock codes array
        :param retry: int, retry number if failed
        :return:
        """
        # errors
        errors = []

        # select host
        host = self._hosts.get()
        # retry to get quote of stocks
        while host and retry>0:
            try:
                 # make request url
                url = self._makeurl(host.host, codes)

                # request remote service
                stime = time.time()
                resp = requests.get(url, headers=Agent.HEADERS, timeout=self._timeout)
                etime = time.time()

                # parse response
                result = self._parse(resp.text)

                # add host succeed
                host.addsucceed(etime-stime)

                return result

            except Exception as e:
                # disable current host
                error = host.host+":"+str(e)
                host.addfailed(error)
                errors.append(errors)

                # pick next host
                host = self._hosts.get()

                # decrease retry count
                retry -= 1

        raise Exception(str(errors))

    def hosts(self):
        """
            get hosts for agent
        :return:
        """
        return self._hosts

    def _makeurl(self, host, codes):
        """
            make request url by stock codes
        :param codes:
        :return:
        """
        # make url
        sina_quote_url = "http://"+host+"/rn="+Agent._makern()+"&list="

        return sina_quote_url+",".join(Agent._addse(codes))

    @staticmethod
    def _makern():
        return digit.strbasen(round(random.random()*60466176), 36)

    @staticmethod
    def _addse(codes):
        """
            add securities exchange flag before stock codes, like: 000001->sz000001
        :param codes: array, stock codes
        :return:
            array, stock codes with exchange flag
        """
        ncodes = []
        for code in codes:
            ncodes.append(stock.addse(code))
        return ncodes

    @staticmethod
    def _parse(text):
        """
            parse response text
        :param text:
        :return:
        """
        # parse results
        results =[]

        try:
            # alias for item
            alias = {
                "jkj": 1, "zsj": 2, "dqj": 3, "zgj": 4, "zdj": 5,
                "cjl": 8, "cje": 9,
                "mrl1": 10, "mrj1": 11, "mrl2": 12, "mrj2": 13, "mrl3": 14, "mrj3": 15, "mrl4": 16, "mrj4": 17, "mrl5": 18, "mrj5": 19,
                "mcl1": 20, "mcj1": 21, "mcl2": 22, "mcj2": 23, "mcl3": 24, "mcj3": 25, "mcl4": 26, "mcj4": 27, "mcl5": 28, "mcj5": 29,
                "date": 30, "time": 31
            }

            # parse all response quotes
            quotes = text.strip().split('\n')

            # parse each quote
            for quote in quotes:
                items = quote.split(',')

                # stock code
                code = items[0].split('=')[0][-6:]

                qte = {}
                # stock quote
                for k in alias:
                    qte[k] = items[alias[k]]

                # process date&time
                qte['time'] = qte['date']+" "+qte['time']
                del qte['date']

                # add to results
                results.append({'code': code, 'quote': Agent._tidy(qte)})
        except Exception as e:
            results = None

        return results

    def _tidy(quote):
        """
            tidy quote data
        :param quote:
        :return:
        """
        # prices
        prices = ["jkj", "zsj", "dqj", "zgj", "zdj", "cje", "mrj1", "mrj2", "mrj3", "mrj4", "mrj5", "mcj1", "mcj2", "mcj3", "mcj4", "mcj5"]

        # volumes
        volumes = ["cjl", "mrl1", "mrl2", "mrl3", "mrl4", "mrl5", "mcl1", "mcl2", "mcl3", "mcl4", "mcl5"]

        # tidy prices
        for p in prices:
            if quote.get(p) is not None:
                quote[p] = str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

        # tidy volumes
        for v in volumes:
            if quote.get(v) is not None:
                quote[v] = str(math.floor(int(quote[v])/100))

        return quote