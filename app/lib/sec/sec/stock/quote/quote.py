"""
    quote base class
"""
import time
from sec.stock.quote import monitor, config


class Quote:
    def __init__(self, id, name, agent):
        """
            init quote
        :param id: str, quote source id, e.g. 'sina'
        :param name: str, quote source name, e.g. '新浪'
        :param agent: str, quote request agent
        """
        self._id = id
        self._name = name

        self._agent = agent

        self._monitor = monitor.Monitor()

    def test(self, code, host):
        """
            try to get quote from specified host(may disabled), if succeed the host will be enabled,
            used to restart a disabled agent host
        :param code: str, stock code
        :param host: str, host in agent
        :return:
        """
        try:
            return self._agent.test(code, host)
        except:
            return None

    def get(self, code, retry=config.RETRY):
        """
            get quote of stock
        :param code: str, stock code, like: '000001'
        :param retry: int, retry times when failed
        :return:
        """
        try:
            stime = time.time()
            result = self._agent.get(code, retry)
            etime = time.time()

            self._monitor.add_succeed(etime - stime)
            return result
        except Exception as e:
            self._monitor.add_failed(str(e))
            return None

    def gets(self, codes, retry=config.RETRY):
        """
            get quote of stocks
        :param codes: array, stock codes, like: ['000001', '300218', '601318']
        :param retry: int, retry times when failed
        :return:
        """
        try:
            stime = time.time()
            result = self._agent.gets(codes, retry)
            etime = time.time()
            self._monitor.add_succeed(etime-stime)
            return result
        except Exception as e:
            self._monitor.add_failed(str(e))
            return None

    def status(self):
        """
            get quote status
        :return:
        """
        s = {
            'id': self._id,
            'name': self._name,
            'succeed': self._monitor.succeed,
            'failed': self._monitor.failed,
            'avgtime': self._monitor.avgtime,
            'ctime': self._monitor.starttime
        }

        return s

    def detail(self):
        """
            get quote source detail
        :return:
        """
        return self._agent.hosts().status()

    def failures(self):
        """
            get lastest failures
        :return:
        """
        return self._monitor.failures

    def __str__(self):
        return str(self.status()) + "\n" + str(self.detail()) +"\n" + str(self.failures()) + "\n"

    __repr__ = __str__