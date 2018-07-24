"""
    parse response
"""
import math, decimal
from lib.stock.quote.level5 import error


def tidy(quote):
    """
        tidy quote data
    :param quote:
    :return:
    """
    # prices
    prices = ["jkj", "zsj", "dqj", "zgj", "zdj", "cje", "mrj1", "mrj2", "mrj3", "mrj4", "mrj5", "mcj1", "mcj2", "mcj3", "mcj4", "mcj5"]

    # volumes
    volumes = ["cjl", "mrl1", "mrl2", "mrl3", "mrl4", "mrl5", "mcl1", "mcl2", "mcl3", "mcl4", "mcl5"]

    # tidy prices
    for p in prices:
        if quote.get(p) is not None:
            quote[p] = round(float(quote[p]),2) #str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

    # tidy volumes
    for v in volumes:
        if quote.get(v) is not None:
            quote[v] = math.floor(int(quote[v]) / 100)

    return quote


def parse(text):
    """
        parse response text
    :param text:
    :return:
    """
    try:
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

            # process date&time
            qte['time'] = qte['date'] + " " + qte['time']
            del qte['date']

            # tidy quote
            qte = tidy(qte)

            # compute ztj&dtj
            qte['ztj'] = round(qte['zsj'] * 1.1, 2)
            qte['dtj'] = round(qte['zsj'] * 0.9, 2)

            # add to results
            results.append({'code': code, 'quote': qte})

        return results
    except Exception as e:
        err = text + "|" + str(e)
        raise error.ParseError(err)
