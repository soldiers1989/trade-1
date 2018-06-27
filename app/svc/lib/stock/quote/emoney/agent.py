"""
    agent to eastmoney quote data
"""
import math, decimal, requests, json, time
from lib.stock.util import stock
from lib.stock.quote import host


class Agent:
    # eastmoney quote server host
    HOST = "nuff.eastmoney.com"
    # request headers
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "nuff.eastmoney.com",
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

        # add header referer
        headers = Agent.HEADERS
        headers.update({"Referer": "http://quote.eastmoney.com/" + stock.addse(code) + ".html"})
        # request
        resp = requests.get(url, headers=headers, timeout=self._timeout)

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
        # add header referer
        headers = Agent.HEADERS
        headers.update({"Referer": "http://quote.eastmoney.com/" + stock.addse(code) + ".html"})

        # errors
        errors = []
        # retry to get quote of stocks
        while retry > 0:
            # select host
            host = self._hosts.get()
            try:
                # make request url
                url = self._makeurl(host.host, code)
                if url:
                    # request remote service
                    stime = time.time()
                    resp = requests.get(url, headers=headers, timeout=self._timeout)
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
                error = host.host + ": " + str(e)
                host.addfailed(error)
                errors.append(error)

        raise Exception(str(errors))

    def gets(self, codes, retry):
        """
            get quote of stocks
        :param codes: array, stock codes array
        :param retry: int, retry number if failed
        :return:
        """
        results = []
        for code in codes:
            results.append(self.get(code, retry))
        return results

    def hosts(self):
        """
            get hosts for agent
        :return:
        """
        return self._hosts

    def _makeurl(self, host, code):
        """
            make request url by stock codes
        :param codes:
        :return:
        """
        # generate id by code
        id = code+"1" if stock.getse(code) == 'sh' else code+"2"

        # generate token
        token = "4f1862fc3b5e77c150a2b985b12db0fd"

        # add random parameter
        rd = str(int(time.time()*1000))

        # make url
        url = "http://"+host+"/EM_Finance2015TradeInterface/JS.ashx?id="+id+"&token="+"&_="+rd

        return url

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
            "jkj": 28, "zsj": 34, "dqj": 25, "zgj": 30, "zdj": 32,
            "cjl": 31, "cje": 35,
            "mrl1": 13, "mrj1": 3, "mrl2": 14, "mrj2": 4, "mrl3": 15, "mrj3": 5, "mrl4": 16, "mrj4": 6, "mrl5": 17, "mrj5": 7,
            "mcl1": 18, "mcj1": 8, "mcl2": 19, "mcj2": 9, "mcl3": 20, "mcj3": 10, "mcl4": 21, "mcj4": 11, "mcl5": 22, "mcj5": 12,
            "time": 49,
        }

        # parse response quote
        rpos = text.find('(')+1
        text = text[rpos:].rstrip().rstrip(')')

        # quote items
        items = json.loads(text)['Value']
        # stock code
        code = items[1]

        qte = {}
        # stock quote
        for k in alias:
            qte[k] = items[alias[k]]

        # process cje
        unit = qte['cje'][-1:]
        unit = 100000000 if unit=='亿' else 10000 if unit =='万' else 1
        qte['cje'] = str(decimal.Decimal(qte['cje'][:-1]) * unit)

        # make result
        result = {"code": code, "quote": qte}

        return result

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