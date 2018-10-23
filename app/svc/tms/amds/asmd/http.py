"""
    http request definition using <requests> module, define a http client using multi sessions, each
    session with different remote hosts
"""
import threading, time, requests


# remote server error
class ServerError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err


# retry limit error
class RetryLimitError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err


class Session:
    """
        session for a base url
    """
    def __init__(self, baseurl, **kwargs):
        """
            init a http client with base url
            kwargs:
            - maxfailed, int, maxfailed limit for client request, default 3
        :param baseurl: str, base url with protocol http/https, Notice: without last path '/'
        """
        self._baseurl = baseurl

        self._headers = kwargs.get('headers')
        self._timeout = kwargs.get('timeout')

        self._maxfailed = kwargs.get('maxfailed', 3)

        self._succeed = 0
        self._timeused = 0.0

        self._failed = 0
        self._cfailed = 0
        self._failure = None

        self._disabled = False

        self._ctime = time.time()

        # lock for host
        self._lock = threading.RLock()

    def get(self, path, **kwargs):
        """
            http request
            kwargs:
            - params, dict, parameters for requests
            - headers, dict, headers for requests
            - timeout, int, connect time out in seconds, default 3s
        :param path:
        :return:
        """
        return self.request('get', path, **kwargs)

    def post(self, path, **kwargs):
        """
            http request
        :param path:
        :return:
        """
        return self.request('post', path, **kwargs)

    def request(self, method, path, **kwargs):
        """
            http request
        :param path:
        :return:
        """
        try:
            # add headers for request
            if self._headers is not None and kwargs.get('headers') is None:
                kwargs['headers'] = self._headers

            # add args for request
            if self._timeout is not None and kwargs.get('timeout') is None:
                kwargs['timeout'] = self._timeout

            # make url
            url = self._baseurl+path

            # make request
            stime = time.time()
            if method == 'get':
                resp = self._get(url, **kwargs)
            else:
                resp = self._post(url, **kwargs)
            etime = time.time()

            # add succeed counter
            self.addsucceed(etime-stime)

            # return resp
            return resp
        except ServerError as e:
            # add failed counter
            self.addfailed(str(e))
            # raise Exception
            raise e

    def _get(self, url, **kwargs):
        """
            send a http get request
        :param url: str, remote resource url
        :return:
            requests response object
        """
        try:
            return requests.get(url, **kwargs)
        except Exception as e:
            raise  ServerError(str(e))

    def _post(self, url, **kwargs):
        """
            send a http post request
        :param url: str, remote resource url
        :return:
            requests response object
        """
        try:
            return requests.post(url, **kwargs)
        except Exception as e:
            raise  ServerError(str(e))

    def addfailed(self, failure):
        """
            add failed
        :param failure:
        :return:
        """
        with self._lock:
            self._failed += 1
            self._cfailed += 1

            if(self._cfailed > self._maxfailed):
                self._disabled = True

            self._failure = failure

    def addsucceed(self, timeused):
        """
            add succeed counter
        :param timeused:
        :return:
        """
        with self._lock:
            self._succeed += 1
            self._cfailed = 0
            self._timeused += timeused
            self._disabled = False
            self._failure = None

    def status(self):
        # average time for succeed request
        avgtime = self._timeused / self._succeed if self._succeed > 0 else 0.0

        s = {
            'baseurl': self._baseurl,
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

    def re_enable(self):
        """
            re enable session
        :return:
        """
        with self._lock:
            self._cfailed = 0
            self._disabled = False
            self._failure = None

    def __str__(self):
        return str(self.status())

    __repr__ = __str__


class Client:
    def __init__(self, baseurls, **kwargs):
        """
            init http client with base urls, and kwargs may be:
            - maxfailed, int, max failed limit for session, then session will be disabled default 3
            - retry, int, max retry limit when request failed, default 3
        :param baseurls: array, host array, like: ['https://192.168.12.1:80', 'http://hq.sinajs.cn', 'http://192.168.1.45']
        """
        # init client sessions
        self._sessions = []
        for baseurl in baseurls:
            self._sessions.append(Session(baseurl, **kwargs))

        # retry limit for request data
        self._retry = kwargs.get('retry', 3)

        # session count
        self._count = len(self._sessions)

        # session roll index
        self._index = 0

    def get(self, path, **kwargs):
        """
            http get with specified session by round robin rules
        :param path: str, remote resource path
        :return:
            requests response object
        """
        return self._request('get', path, **kwargs)

    def post(self, path, **kwargs):
        """
            http post with specified session by round robin rules
        :param path: str, remote resource path
        :return:
            requests response object
        """
        return self._request('post', path, **kwargs)

    def _request(self, method, path, **kwargs):
        """
            http request with specified session by round robin rules
        :param path: str, remote resource path
        :return:
            requests response object
        """
        # get retry count
        retry = self._retry

        # select a usable session
        session = self.next_session()

        # request until retry limit
        while retry > 0:
            try:
                if session is None:
                    self.re_enable()
                    raise ServerError('request: %s failed, no usable remote hosts' % path)
                if method == 'get':
                    return session.get(path, **kwargs)
                else:
                    return session.post(path, **kwargs)
            except ServerError as e:
                # select next session
                session = self.next_session()

                # decrease retry count
                retry -= 1

        # retry limit
        raise RetryLimitError('request: %s failed, max retry limit reached' % str(self._retry))

    def status(self):
        """
            get host status
        :return:
        """
        results = []

        for session in self._sessions:
            results.append(session.status())

        return results

    def next_session(self):
        """
            get next usable session
        :return:
        """
        for i in range(0, self._count):
            session = self._sessions[self._index%self._count]
            self._index += 1
            if not session.disabled:
                return session
        return None

    def re_enable(self):
        """
            reset
        :return:
        """
        for session in self._sessions:
            session.re_enable()

    def __str__(self):
        return str(self.status())

    __repr__ = __str__
