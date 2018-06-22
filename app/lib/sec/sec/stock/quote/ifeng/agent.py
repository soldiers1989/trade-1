"""
    agent to ifeng quote data
"""
import math, decimal, requests, json, random, time
from sec.util import stock
from sec.stock.quote import host


class Agent:
    # ifeng quote server host
    HOST = "hq.finance.ifeng.com"
    # request headers
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "hq.finance.ifeng.com",
        "Referer": "http://finance.ifeng.com/app/hq/"
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
            request quote of stock @code from ifeng quote url
        :param code: str, stock code
        :param retry: int, retry number if failed
        :return:
        """
        return self.gets([code], retry)[0]

    def gets(self, codes, retry):
        """
            get quote of stocks
        :param codes: array, stock codes array
        :param retry: int, retry number if failed
        :return:
        """
        # errors
        errors = []
        # retry to get quote of stocks
        while retry>0:
            # select host
            host = self._hosts.get()
            try:
                 # make request url
                url = self._makeurl(host.host, codes)
                if url:
                    # request remote service
                    stime = time.time()
                    resp = requests.get(url, headers=Agent.HEADERS, timeout=self._timeout)
                    etime = time.time()

                    # parse response
                    result = self._parse(resp.text)

                    # add succeed for host
                    host.addsucceed(etime-stime)

                    return result
                else:
                    raise Exception('not host can be used')
            except Exception as e:
                retry -= 1
                error = host.host+": "+str(e)
                host.addfailed(error)
                errors.append(error)

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
        ifeng_quote_url = "http://"+host+"/q.php?l="

        return ifeng_quote_url+",".join(Agent._addse(codes))+"&f=json&r="+str(random.random())

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
        results = []

        # alias for item
        alias = {
            "jkj": 4, "zsj": 1, "dqj": 0, "zgj": 5, "zdj": 6,
            "cjl": 9, "cje": 10,
            "mrl1": 16, "mrj1": 11, "mrl2": 17, "mrj2": 12, "mrl3": 18, "mrj3": 13, "mrl4": 19, "mrj4": 14, "mrl5": 20, "mrj5": 15,
            "mcl1": 26, "mcj1": 21, "mcl2": 27, "mcj2": 22, "mcl3": 28, "mcj3": 23, "mcl4": 29, "mcj4": 24, "mcl5": 30, "mcj5": 25,
            "time": 34,
        }

        # parse all response quotes
        rpos = text.find('=')+1
        text = text[rpos:].rstrip().rstrip(';')
        quotes = json.loads(text)

        # parse each quote
        for stock in quotes:
            # stock code
            code = stock[-6:]

            # quote items
            items = quotes[stock]

            qte = {}
            # stock quote
            for k in alias:
                qte[k] = items[alias[k]]

            # translate time from unix timestamp to datetime
            qte['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(qte['time']))

            # add to results
            results.append({'code': code, 'quote': Agent._tidy(qte)})

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