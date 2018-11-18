"""
    remote task manager
"""
import time
from . import task
from .. import timer


class TaskManager:
    def __init__(self):
        """
            init task manager
        """
        self._tasks = {}

    def add(self, id, code, name, cond, method, url, data=None, json=None, stopped=True, exclusive=True, maxkeep=20, ctime=int(time.time()), mtime=int(time.time())):
        """
            add a new timer task
        :param id: str, timer task id
        :param code: str, timer task code
        :param name: str, timer task name
        :param cond: str, timer condition
        :param method: str, post or get
        :param url: str, remote url
        :param data: str, post data for remote url
        :param json: str, post json data for remote urls
        :param exclusive: bool, exclusive for same id task
        :param maxkeep: int, max record keep for timer task execute log
        :return:
        """
        # create new remote runnable task
        remotetask = task.RemoteTask(id, code, name, method, url, data=None, json=None, ctime=ctime, mtime=mtime)

        # add to timer
        timer.default.add(id, name, cond, remotetask, stopped, exclusive, maxkeep)

    def delete(self, id):
        """
            delete a timer task
        :param id:
        :return:
        """
        timer.default.delete(id)

    def clear(self):
        """
            clear all timer tasks
        :return:
        """
        timer.default.clear()

    def exist(self, id):
        """
            check if task with id has exist
        :param id:
        :return:
        """
        return timer.default.exist(id)

    def enable(self, id):
        """
            enable a time task
        :param id:
        :return:
        """
        timer.default.enable(id)

    def disable(self, id):
        """
            disable a timer task
        :param id:
        :return:
        """
        timer.default.disable(id)

    def execute(self, id):
        """
            execute a timer task
        :param id:
        :return:
        """
        timer.default.execute(id)

    def notify(self, id, seq, status, result):
        """
            notify remote execute result
        :param id:
        :param seq:
        :param status:
        :param result:
        :return:
        """
        timer.default.notify(id, seq, status, result)

    def status(self, id=None):
        """
            get task status
        :param id:
        :return:
        """
        return timer.default.status(id)

    def detail(self, id):
        """
            get detail information
        :param id:
        :return:
        """
        return timer.default.detail(id)
