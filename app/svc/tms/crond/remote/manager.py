"""
    remote task manager
"""
from . import task
from .. import timer


class TaskManager:
    def __init__(self):
        """
            init task manager
        """
        self._tasks = {}

    def add(self, id, name, cond, url, exclusive=True, maxkeep=20):
        """

        :param id:
        :param name:
        :param cond:
        :param url:
        :param exclusive:
        :param maxkeep:
        :return:
        """
        # create new remote runnable task
        remotetask = task.RemoteTask(id, name, url)

        # add to timer
        timer.default.add(id, name, cond, remotetask, exclusive, maxkeep)

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

    def status(self, id):
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
