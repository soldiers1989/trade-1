"""
    agent to sina quote data
"""
import requests
from sec.util import stock


class Agent:
    def __init__(self, timeout):
        self._timeout = timeout

    def get(self, code):
        """
            request quote of stock @code from sina quote url
        :param code:
        :return:
        """
        return self.gets([code])[0]

    def gets(self, codes):
        """

        :param codes:
        :return:
        """
        # make request url
        url = self._makeurl(codes)

        # request remote service
        resp = requests.get(url, timeout=self._timeout)

        # parse response
        return self._parse(resp.text)

    @staticmethod
    def _makeurl(codes):
        """
            make request url by stock codes
        :param codes:
        :return:
        """
        sina_quote_url = "http://hq.sinajs.cn/list="
        return sina_quote_url+",".join(Agent._addse(codes))

    @staticmethod
    def _addse(codes):
        """
            add securities exchange flag before stock codes, like: 000001->sz000001
        :param codes: array, stock codes
        :return:
            array, stock codes with exchange flag
        """
        ncodes = []
        for code in codes:
            ncodes.append(stock.addse(code))
        return ncodes

    @staticmethod
    def _parse(text):
        """
            parse response text
        :param text:
        :return:
        """
        # parse results
        results = []

        # alias for item
        alias = {
            "jkj": 1, "zsj": 2, "dqj": 3, "zgj": 4, "zdj": 5,
            "cjl": 8, "cje": 9,
            "mrl1": 10, "mrj1": 11, "mrl2": 12, "mrj2": 13, "mrl3": 14, "mrj3": 15, "mrl4": 16, "mrj4": 17, "mrl5": 18, "mrj5": 19,
            "mcl1": 20, "mcj1": 21, "mcl2": 22, "mcj2": 23, "mcl3": 24, "mcj3": 25, "mcl4": 26, "mcj4": 27, "mcl5": 28, "mcj5": 29,
            "date": 30, "time": 31
        }

        # parse all response quotes
        quotes = text.strip().split('\n')

        # parse each quote
        for quote in quotes:
            items = quote.split(',')

            # stock code
            code = items[0].split('=')[0][-6:]

            qte = {}
            # stock quote
            for k in alias:
                qte[k] = items[alias[k]]

            # add to results
            results.append({'code': code, 'quote': qte})

        return results
