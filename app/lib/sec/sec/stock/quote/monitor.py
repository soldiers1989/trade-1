"""
    monitor for quote data sources
"""
import time


class Monitor:
    """
        monitor
    """
    def __init__(self):
        self._start = time.time() # monitor start time

        self._total = 0 # total request
        self._succeed = 0 # total succeed request
        self._failed = 0 # total failed request

        self._failures = [] # latest failures

    @property
    def starttime(self):
        return self._start

    @property
    def total(self):
        return self._total

    @property
    def succeed(self):
        return self._succeed

    @property
    def failed(self):
        return self._failed

    @property
    def failures(self):
        return self._failures

    def add_total(self):
        self._total += 1

    def add_succeed(self):
        self._succeed += 1

    def add_failed(self):
        self._failed += 1

    def add_failure(self, reason):
        self._failures.append(reason)

    def clear_failures(self):
        self._failures = []
