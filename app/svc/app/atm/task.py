"""
    task base class
"""
import time, threading, requests, logging
from . import error


class _Callback:
    def __init__(self, url):
        self._url = url

    def notify(self, status, result):
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
    """
        task base class
    """
    # task execute result
    SUCCESS, FAILED = 1, 0

    def __init__(self, *args, **kwargs):
        """
            init task
        :param args:
        :param kwargs:
        """
        # task info
        self._ctime = None
        self._stime = None
        self._etime = None
        self._result = None

        # stop flag
        self._stopped = False

        # remote callback url after task has stopped or finished
        self._callback = _Callback(kwargs.get('callback'))

        # init super thread
        super().__init__(*args, **kwargs)

    def cname(self):
        """
            get instance class name
        :return:
        """
        return self.__class__.__name__

    def stop(self):
        """
            stop task
        :return:
        """
        self._stopped = True

    def execute(self):
        """
            subclass must implements this method
        :return:
        """
        pass

    def status(self):
        """
            get task status informations
        :return:
            dict
        """
        return {
            'name': self.__class__.__name__,
            'ctime': self._ctime,
            'stime': self._stime,
            'etime': self._etime,
            'result': self._result
        }

    def run(self):
        """
            thread function
        :return:
        """
        try:
            self._stime = int(time.time())

            taskname = self.__class__.__name__
            logging.info('start task: %s' % taskname)
            result = self.execute()
            logging.info('finish task: %s, result: %s' % (taskname, str(result)))
            self.notify(Task.SUCCESS, result)

            self._etime = int(time.time())
            self._result = 'success'
        except Exception as e:
            logging.info('failed task: %s, result: %s' % (taskname, str(e)))
            self.notify(Task.FAILED, str(e))
            self._etime = int(time.time())
            self._result = 'failed'

    def notify(self, status, result):
        """
            callback
        :param status:
        :param result:
        :return:
        """
        self._callback.notify(status, result)


class _Manager(threading.Thread):
    """
        manager for task objects
    """
    MAX_HISTORIES = 100

    def __init__(self, *args, **kwargs):
        """
            init task manager
        :param args:
        :param kwargs:
        """
        # current running task list
        self._tasks = {}

        # task execute histories
        self._histories = []

        # lock for task list
        self._lock = threading.Lock()

        # stop flag for manager thread
        self._stopped = False

        super().__init__(*args, **kwargs)

    def take(self, task:Task, started=False):
        """
            take a new task for managing
        :param id: str, task unique id
        :param task: obj, task object
        :param started: bool, task has started flag
        :return:
        """
        with self._lock:
            # check exist task
            if self._tasks.get(id) is not None:
                raise error.task_has_exist

            # start task
            if not started:
                task.start()

            # add to task list
            self._tasks[id] = task

    def free(self, id:str):
        """
            free a task from manager, stop task
        :param id:
        :return:
        """
        with self._lock:
            # check task existence
            task = self._tasks.get(id)
            if task is None:
                raise error.task_has_not_exist

            # stop task
            task.stop()

    def current(self):
        """
            get current task status
        :return:
        """
        with self._lock:
            results = []
            for t in self._tasks:
                results.append(t.status())
            return results

    def history(self):
        """

        :return:
        """
        with self._lock:
            results = self._histories.copy()
            return results

    def stop(self):
        """
            stop manager
        :return:
        """

    def run(self):
        """
            thread function
        :return:
        """
        while not self._stopped:
            # manage task
            self._manage()

            # sleep for while
            time.sleep(1)

    def _manage(self):
        """
            manage task
        :return:
        """
        with self._lock:
            # finished task list
            finished = []

            # check current task
            for id, t in self._tasks.items():
                # wait task finished
                t.join(0)

                # task has finished
                if not t.isAlive():
                    # record finished
                    finished.append(id)
                    # record history
                    self._histories.append(t.status())

                # check histories length
                if len(self._histories) > self.MAX_HISTORIES:
                    self._histories.pop(0)

            # remote finished tasks from current
            for tid in finished:
                del self._tasks[tid]


# task manager instance
manager = _Manager()