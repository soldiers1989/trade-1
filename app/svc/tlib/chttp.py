"""
    client http for an none block remote request
"""
import time, queue, threading, requests


class _Error(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Callback:
    """
        callback for request
    """
    def on_succeed(self, req, resp):
        """
            request success call back
        :param req: obj, request object
        :param resp: obj, request response object
        :return:
        """
        pass

    def on_failed(self, req, error):
        """
            request failed call back
        :param req: obj, request object
        :param error: str, request failed message
        :return:
        """
        pass


class _Request:
    """
        request object
    """
    GET = 'get'
    POST = 'post'

    def __init__(self, method:str, url:str, params:dict=None, delay:int=0, callback:Callback=None):
        """
            init a http request object
        :param method: str, 'get' or 'post'
        :param url:
        :param params:
        :param delay:
        :param callback:
        """
        if method not in [_Request.GET, _Request.POST]:
            raise _Error('unsupport method: %s' % str(method))

        self.method = method
        self.url = url
        self.params = params
        self.delay = delay
        self.callback = callback
        self.ctime = time.time()

    def expired(self):
        """
            delay time reached
        :return:
        """
        if int(time.time()-self.ctime) > self.delay:
            return True

        return False

    def do(self):
        """
            do the request
        :return:
        """
        try:
            resp = requests.request(self.method, self.url, params=self.params)
            if self.callback is not None:
                self.callback.on_succeed(self, resp)
        except Exception as e:
            self.callback.on_failed(self, str(e))


class CHttp(threading.Thread):
    def __init__(self):
        """
            init client http service
        """
        self._stopped = False
        self._queue = queue.Queue()
        super().__init__()

    def stop(self):
        """
            stop client http service
        :return:
        """
        self._stopped = True

    def get(self, url:str, params:dict=None, delay:int=0, callback:object=None):
        """
            async http get request
        :param url:
        :param params:
        :param delay:
        :param callback:
        :return:
        """
        self._queue.put(_Request(_Request.GET, url, params=params, delay=delay, callback=callback))

    def post(self, url:str, params:dict=None, delay:int=0, callback:object=None):
        """
            async http post request
        :param url:
        :param params:
        :param delay:
        :param callback:
        :return:
        """
        self._queue.put(_Request(_Request.POST, url, params=params, delay=delay, callback=callback))

    def run(self):
        """
            wait request on the queue
        :return:
        """
        while not self._stopped:
            try:
                req = self._queue.get(timeout=1)
                if not req.expired():
                    self._queue.put(req)
                else:
                    req.do()
            except:
                pass


