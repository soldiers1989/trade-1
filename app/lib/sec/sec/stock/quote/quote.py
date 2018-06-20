"""
    quote base class
"""
from sec.stock.quote import monitor


class Quote:
    def __init__(self):
        self.monitor = monitor.Monitor()

    def get(self, code):
        pass

    def gets(self, codes):
        pass
