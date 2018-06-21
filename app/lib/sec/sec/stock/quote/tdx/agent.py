"""
    remote service request wraper
"""
import decimal, requests

from sec.util import stock


class Agent:
    def __init__(self, host, port, servers, timeout):
        """
            init tdx agent
        :param host: str, remote agent host
        :param port: str, remote agent port
        :param servers: array, quote server list, [(ip, port), (ip, port), ...]
        :param timeout: int, connection timeout in seconds
        """
        self._host = host
        self._port = port
        self._servers = servers
        self._timeout = timeout

        # current server index
        self._sindex = 0
        # connect remote quote server
        self.connect()

    def connect(self):
        """
            连接行情服务器
        :param ip: str, in, remote quote server ip
        :param port: int, in, remote quote server port
        :return:
        """
        # status code by agent response
        success = 0

        try:
            # disconnect before connect
            self.disconnect()

            # make request url
            url = "http://%s:%s/connect" % (self._host, self._port)

            # select server
            ip, port = self._server()

            # request parameters
            params = {
                "ip": ip,
                "port" : port
            }

            # request remote service
            resp = requests.get(url, params, timeout=self._timeout).json()

            # get response result
            status, msg = resp["status"], resp["msg"]

            if status != success:
                return False

            return True
        except:
            return False

    def get(self, code):
        """
            查询当前行情
        :param code: str, stock code
        :return:
        """
        # status code by agent response
        success = 0

        # make request url
        url = "http://%s:%s/quote" % (self._host, self._port)

        # request parameters
        params = {
            "zqdm": code,
            "market": self._market(stock.getse(code))
        }

        # request remote service
        resp = requests.get(url, params, timeout=self._timeout).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]

        # check response
        if status != success:
            raise Exception(msg)

        # check data
        if len(data) != 2:
            raise Exception('error response data')

        # make results
        result = {'code': code, 'quote': self._parse(data)}

        return result

    def gets(self, codes):
        """

        :param codes:
        :return:
        """
        results = []
        for code in codes:
            results.append(self.get(code))
        return results

    def disconnect(self):
        """
            断开行情服务器
        :return:
        """

        try:
            # make request url
            url = "http://%s:%s/disconnect" % (self._host, self._port)

            # request parameters
            params = { }

            # request remote service
            resp = requests.get(url, params, timeout=self._timeout)
        except:
            pass

    @staticmethod
    def _parse(data):
        """
            parse
        :param data:
        :return:
        """
        # parse result
        result = {}

        # alias names for response data
        alias = {
            "开盘": 'jkj', "昨收": 'zsj', "现价": 'dqj', "最高": 'zgj', "最低": 'zdj',
            "内盘": 'np', "外盘": 'wp',
            "总量": 'cjl', "总金额": 'cje',
            "买一价": 'mrj1', "买一量": 'mrl1', "买二价": 'mrj2', "买二量": 'mrl2', "买三价": 'mrj3', "买三量": 'mrl3', "买四价": 'mrj4', "买四量": 'mrl4', "买五价": 'mrj5', "买五量": 'mrl5',
            "卖一价": 'mcj1', "卖一量": 'mcl1', "卖二价": 'mcj2', "卖二量": 'mcl2', "卖三价": 'mcj3', "卖三量": 'mcl3', "卖四价": 'mcj4', "卖四量": 'mcl4', "卖五价": 'mcj5', "卖五量": 'mcl5',
        }

        # parse data by alias
        idx = 0
        for column in data[0]:
            value = alias.get(column)
            if value is not  None:
                result[value] = data[1][idx]
            idx += 1

        # tidy result
        result = Agent._tidy(result)

        return result

    @staticmethod
    def _tidy(quote):
        """
            tidy parse result
        :param self:
        :return:
        """
        # prices
        prices = ["jkj", "zsj", "dqj","zgj", "zdj", "cje", "mrj1", "mrj2", "mrj3", "mrj4", "mrj5", "mcj1", "mcj2", "mcj3", "mcj4", "mcj5"]

        # tidy prices
        for p in prices:
            if quote.get(p) is not None:
                quote[p] = str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

        return quote

    @staticmethod
    def _market(se):
        """
            get market by se
        :param se:
        :return:
        """
        if se == 'sz':
            return 0

        if se == 'sh':
            return 1

        return None

    def _server(self):
        """
            select server to connect
        :return:
        """
        sz = len(self._servers)
        server = self._servers[self._sindex%sz]
        self._sindex += 1
        return server
