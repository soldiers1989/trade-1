"""
    error definition for trade service
"""


class TradeError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
