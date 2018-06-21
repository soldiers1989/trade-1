"""
    quote base class
"""
from sec.stock.quote import monitor


class Quote:
    def __init__(self):
        self.monitor = monitor.Monitor()

    def get(self, code, retry=1):
        pass

    def gets(self, codes, retry=1):
        pass

    def alive(self):
        pass