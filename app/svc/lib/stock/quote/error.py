"""
    error for quote
"""


class ParseError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err


class HostLackError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err


class RetryLimitError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err


class VendorLackError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err