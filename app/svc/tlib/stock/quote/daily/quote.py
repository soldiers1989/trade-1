"""
    quote base class
"""
import time, threading


class Quote:
    def __init__(self, id, name, servers):
        """
            init quote
        :param id: str, quote source id, e.g. 'sina'
        :param name: str, quote source name, e.g. '新浪'
        """
        self._id = id
        self._name = name

        self._succeed = 0
        self._timeused = 0.0

        self._failed = 0
        self._cfailed = 0
        self._failure = None

        self._disabled = False
        self._ctime = time.time()

        self.servers = servers

        # lock for variables
        self._lock = threading.RLock()

    def test(self, date):
        """
            try to get quote from specified host(may disabled), if succeed the host will be enabled,
            used to restart a disabled agent host
        :param date: str, date string YYYY-mm-dd
        :return:
        """
        pass

    def fetch(self, date):
        """
            fetch quote of stock
        :param date: str, date string YYYY-mm-dd
        :return:
        """
        pass

    def status(self):
        """
            get quote status
        :return:
        """
        avgtime = self._timeused / self._succeed if self._succeed > 0 else 0.0
        s = {
            'id': self._id,
            'name': self._name,
            'succeed': self._succeed,
            'failed': self._failed,
            'cfailed': self._cfailed,
            'avgtime': avgtime,
            'disabled': self._disabled,
            'ctime': self._ctime,
            'failure': self._failure,
            'servers': self.servers.status()
        }

        return s

    def disable(self):
        """
            disable quote
        :return:
        """
        self._lock.acquire()
        self._disabled = True
        self._lock.release()

    @property
    def disabled(self):
        return self._disabled

    def addfailed(self, failure):
        """
            add failed
        :param failure:
        :return:
        """
        self._lock.acquire()

        self._failed += 1
        self._cfailed += 1
        self._failure = failure

        self._lock.release()

    def addsucceed(self, timeused):
        """
            add succeed counter
        :param timeused:
        :return:
        """
        self._lock.acquire()

        self._succeed += 1
        self._timeused += timeused

        self._cfailed = 0
        self._failure = None

        self._disabled = False

        self._lock.release()

    def __str__(self):
        return str(self.status())

    __repr__ = __str__