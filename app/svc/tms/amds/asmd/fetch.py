"""
    fetcher definition, make a standard normalize on:
        fetch->parse
    operation
"""


class Fetcher:
    """
        fetch base class
    """
    def fetch(self, *args, **kwargs):
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