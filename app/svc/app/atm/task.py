"""
    task
"""
import threading


class Task(threading.Thread):
    def __init__(self, id, type, name):
        self._id = id
        self._type = type
        self._name = name
        self._stime = None
        self._etime = None

        threading.Thread.__init__(self)
