"""
    host for quote
"""
import threading


class Host:
    def __init__(self, host, maxfailed):
        self._host = host
        self._succeed = 0
        self._failed = 0
        self._latest_failed = 0
        self._disabled = False
        self._maxfailed = maxfailed

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
    def latest_failed(self):
        return self._latest_failed

    @property
    def disabled(self):
        return self._disabled

    def addfailed(self):
        self._lock.acquire()

        self._failed += 1
        self._latest_failed += 1
        if(self._latest_failed > self._maxfailed):
            self._disabled = True

        self._lock.release()

    def addsucceed(self):
        self._lock.acquire()

        self._succeed += 1
        self._latest_failed = 0
        self._disabled = False

        self._lock.release()

    def __str__(self):
        s = {"host": self._host, "succeed":self._succeed, "failed":self._failed, "latest_failed":self._latest_failed, "disabled":self._disabled}
        return str(s)

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

    def __str__(self):
        s = []
        for host in self._hosts:
            s.append(str(host))
        return str(s)

    __repr__ = __str__
