"""
    task base class
"""
import threading, requests, logging


class _Callback:
    def __init__(self, url):
        self._url = url

    def execute(self, status, result):
        """
            execute callback by request the remote url
        :param status:
        :param result:
        :return:
        """
        if self._url is None:
            return

        try:
            # extra parameters
            params = {
                'status': status,
                'result': result
            }

            # remote callback
            requests.get(self._url, params=params)

            # add log
            logging.info('callback: %s, status: %s, result: %s', (self._url, str(status), str(result)))
        except Exception as e:
            logging.error(str(e))


class Task(threading.Thread):
    # task execute result
    SUCCESS, FAILED = 1, 0

    def __init__(self, callback):
        self._callback = _Callback(callback)
        super().__init__()

    def execute(self):
        pass

    def run(self):
        """
            thread function
        :return:
        """
        taskname = self.__class__.__name__
        try:
            logging.info('start task: %s' % taskname)
            result = self.execute()
            logging.info('finish task: %s, result: %s' % (taskname, str(result)))
            self.notify(Task.SUCCESS, result)
        except Exception as e:
            logging.info('failed task: %s, result: %s' % (taskname, str(e)))
            self.notify(Task.FAILED, str(e))

    def notify(self, status, result):
        """
            callback
        :param status:
        :param result:
        :return:
        """
        self._callback.execute(status, result)