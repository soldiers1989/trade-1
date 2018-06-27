"""
    host for quote
"""
import threading, time


class Host:
    def __init__(self, host, maxfailed):
        self._ctime = time.time()

        self._host = host
        self._maxfailed = maxfailed

        self._succeed = 0
        self._failed = 0
        self._cfailed = 0
        self._time = 0.0
        self._failures = []

        self._disabled = False

        # lock for host
        self._lock = threading.RLock()

    @property
    def host(self):
        return self._host

    @property
    def succeed(self):
        return self._succeed

    @property
    def failed(self):
        return self._failed

    @property
    def cfailed(self):
        return self._cfailed

    @property
    def avgtime(self):
        return self._time / self._succeed if self._succeed > 0 else 0.0

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
        if(self._cfailed > self._maxfailed):
            self._disabled = True

        self._failures.append(failure)

        self._lock.release()

    def addsucceed(self, timeused):
        self._lock.acquire()

        self._succeed += 1
        self._cfailed = 0
        self._time += timeused
        self._disabled = False
        self._failures = []

        self._lock.release()

    def status(self):
        s = {
            'id': self._host,
            'name': self._host,
            'succeed': self._succeed,
            'failed': self._failed,
            'cfailed': self._cfailed,
            'disabled': self._disabled,
            'avgtime': self.avgtime,
            'ctime': self._ctime

        }

        return s

    def __str__(self):
        return str(self.status())

    __repr__ = __str__


class Hosts:
    def __init__(self, hosts, maxfailed=3):
        """
            init hosts
        :param hosts: array, host array, like: ['192.168.12.1:80', 'hq.sinajs.cn', '192.168.1.45']
        :param maxfailed: int, kickout host when max latest failed time reached for host
        """
        # init hosts
        self._hosts = []
        for host in hosts:
            self._hosts.append(Host(host, maxfailed))

        # hosts count
        self._count = len(self._hosts)

        # host roll index
        self._index = 0


    def all(self):
        """
            get all hosts
        :return:
        """
        return self._hosts

    def find(self, host):
        """
            find host object by host name
        :param name:
        :return:
        """
        for h in self._hosts:
            if h.host == host:
                return h

        return None

    def get(self):
        """
            get a host by round robin rules
        :return:
        """
        # select a usable host
        for i in range(0, self._count):
            host = self._hosts[self._index%self._count]
            self._index += 1
            if not host.disabled:
                return host

        # no host can be used
        return None

    def status(self):
        """
            get host status
        :return:
        """
        results = []

        for host in self._hosts:
            results.append(host.status())

        return results

    def __str__(self):
        return str(self.status())

    __repr__ = __str__
