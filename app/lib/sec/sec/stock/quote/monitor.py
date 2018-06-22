"""
    monitor for quote data sources
"""
import time, threading


class Monitor:
    """
        monitor
    """
    def __init__(self):
        self._start = time.time() # monitor start time

        # total succeed request
        self._succeed = 0
        # total times used for succeed request in seconds
        self._time = 0.0
        # total failed request
        self._failed = 0

        # latest failures
        self._failures = []

        # lock for variables
        self._lock = threading.RLock()

    @property
    def starttime(self):
        return self._start

    @property
    def succeed(self):
        return self._succeed

    @property
    def failed(self):
        return self._failed

    @property
    def avgtime(self):
        return self._time/self._succeed if self._succeed>0 else 0.0

    @property
    def failures(self):
        return self._failures


    def add_succeed(self, timeused):
        self._lock.acquire()
        self._succeed += 1
        self._time += timeused
        self._failures = []
        self._lock.release()

    def add_failed(self, reason):
        self._lock.acquire()
        self._failed += 1
        self._failures.append(reason)
        self._lock.release()

    def __str__(self):
        return "succeed: "+self._succeed+", failed: "+self._failed+", avgtime: "+self.avgtime + "\n" + str(self._failures)+"\n"

    __repr__ = __str__
