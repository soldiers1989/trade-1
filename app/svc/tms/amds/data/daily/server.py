"""
    host for quote
"""
import json, threading, time, requests, requests.exceptions

from requests.exceptions import Timeout, ConnectionError

from . import error


class Server:
    def __init__(self, host, timeout, maxfailed):
        self._host = host
        self._baseurl = 'http://'+host

        self._timeout = timeout
        self._maxfailed = maxfailed

        self._succeed = 0
        self._timeused = 0.0

        self._failed = 0
        self._cfailed = 0
        self._failure = None

        self._disabled = False

        self._ctime = time.time()

        # lock for host
        self._lock = threading.RLock()

    def test(self, path, headers):
        """
            test server
        :return:
        """
        result = None
        try:
            resp = self.get(path, headers).text
            result = {'host': self._host, 'status': 0, 'msg': 'success', 'data': resp}
        except Exception as e:
            result = {'host': self._host, 'status': -1, 'msg': str(e), 'data': None}

        return resp

    def get(self, path, headers):
        """
            http request
        :param path:
        :return:
        """
        try:
            # make url
            url = self._baseurl+path

            # make request
            stime = time.time()
            resp = requests.get(url, headers=headers, timeout=self._timeout)
            etime = time.time()

            # add succeed counter
            self.addsucceed(etime-stime)

            # return resp
            return resp
        except (Timeout,ConnectionError) as e:
            err = json.dumps(str(e))
            # add failed counter
            self.addfailed(err)
            # raise Exception
            raise error.ServerError(err)

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
        self._cfailed = 0
        self._timeused += timeused
        self._disabled = False
        self._failure = None

        self._lock.release()

    def status(self):
        # average time for succeed request
        avgtime = self._timeused / self._succeed if self._succeed > 0 else 0.0

        s = {
            'host': self._host,
            'succeed': self._succeed,
            'failed': self._failed,
            'cfailed': self._cfailed,
            'disabled': self._disabled,
            'avgtime': avgtime,
            'ctime': self._ctime,
            'failure': self._failure
        }

        return s

    @property
    def disabled(self):
        return self._disabled

    def __str__(self):
        return str(self.status())

    __repr__ = __str__


class Servers:
    def __init__(self, hosts, timeout, maxfailed):
        """
            init hosts
        :param hosts: array, host array, like: ['192.168.12.1:80', 'hq.sinajs.cn', '192.168.1.45']
        :param maxfailed: int, kickout host when max latest failed time reached for host
        """
        # init hosts
        self._servers = []
        for host in hosts:
            self._servers.append(Server(host, timeout, maxfailed))

        # hosts count
        self._count = len(self._servers)

        # host roll index
        self._index = 0

    def test(self, path, headers):
        """
            test servers
        :param path:
        :return:
        """
        results = []
        for server in self._servers:
            resp = server.test(path, headers)
            results.append(resp)
        return results


    def get(self, path, headers, retry):
        """
            get a host by round robin rules
        :return:
        """
        # select a usable server
        server = self.nexts()

        # request until retry limit
        while retry > 0:
            try:
                if server is None:
                    raise error.NoneServerError('none server can be used')

                return server.get(path, headers)
            except error.ServerError as e:
                # select next server
                server = self.nexts()

                # decrease retry count
                retry -= 1

        # retry limit
        raise error.RetryLimitError('retry limit '+str(retry))

    def status(self):
        """
            get host status
        :return:
        """
        results = []

        for server in self._servers:
            results.append(server.status())

        return results

    def nexts(self):
        """
            get next usable server
        :return:
        """
        for i in range(0, self._count):
            server = self._servers[self._index%self._count]
            self._index += 1
            if not server.disabled:
                return server
        return None

    def __str__(self):
        return str(self.status())

    __repr__ = __str__
