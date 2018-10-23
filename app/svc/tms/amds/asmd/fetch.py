"""
    fetcher definition, make a standard normalize on:
        fetch->parse
    operation
"""


class Fetcher:
    def __init__(self):
        pass

    def fetch(self):
        pass

    @staticmethod
    def json(text):
        """
        解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
        :param expr:非标准JSON的Javascript字符串
        :return:Python字典
        """
        obj = eval(text, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
        return obj