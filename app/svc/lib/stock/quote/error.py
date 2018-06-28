"""
    error for quote
"""


# server error
class ServerError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err


# client request error
class RequestError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err


# parse server response error
class ParseError(Exception):
    def __init__(self, err):
        self._err = err

    def __str__(self):
        return self._err


# none server can be used
class NoneServerError(Exception):
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
