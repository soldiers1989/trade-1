"""
    remote service request wraper
"""
import requests

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

        self._sindex = 0 # current server index

    def get(self, code):
        """
            查询当前行情
        :param market: str, in, 0 - shenzhen, 1 - shanghai
        :param zqdm: str, in, stock code
        :return:
        """
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
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def gets(self, codes):
        """

        :param codes:
        :return:
        """
        results = []
        for code in codes:
            results.append(self.get(code))
        return results

    def _market(self, se):
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


    def _connect(self):
        """
            连接行情服务器
        :param ip: str, in, remote quote server ip
        :param port: int, in, remote quote server port
        :return:
        """
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
        status = True if status is 0 else False

        # return response result
        return status, msg


    def _disconnect(self):
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
            resp = requests.get(url, params, timeout=self._timeout).json()

            # get response result
            status, msg = resp["status"], resp["msg"]
            status = True if status is 0 else False

            # return response result
            return status, msg
        except Exception as e:
            return False, str(e)
