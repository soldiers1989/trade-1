"""
    parser for easy money quote response
"""
import json, math, decimal


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
            quote[p] = str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

    # tidy volumes
    for v in volumes:
        if quote.get(v) is not None:
            quote[v] = str(math.floor(int(quote[v]) / 100))

    return quote


def parse(text):
    """
        parse response text
    :param text:
    :return:
    """
    # parse results
    results = []

    # alias for item
    alias = {
        "jkj": 28, "zsj": 34, "dqj": 25, "zgj": 30, "zdj": 32,
        "cjl": 31, "cje": 35,
        "mrl1": 13, "mrj1": 3, "mrl2": 14, "mrj2": 4, "mrl3": 15, "mrj3": 5, "mrl4": 16, "mrj4": 6, "mrl5": 17, "mrj5": 7,
        "mcl1": 18, "mcj1": 8, "mcl2": 19, "mcj2": 9, "mcl3": 20, "mcj3": 10, "mcl4": 21, "mcj4": 11, "mcl5": 22, "mcj5": 12,
        "time": 49,
    }

    # parse response quote
    rpos = text.find('(') + 1
    text = text[rpos:].rstrip().rstrip(')')

    # quote items
    items = json.loads(text)['Value']
    # stock code
    code = items[1]

    qte = {}
    # stock quote
    for k in alias:
        qte[k] = items[alias[k]]

    # process cje
    unit = qte['cje'][-1:]
    unit = 100000000 if unit == '亿' else 10000 if unit == '万' else 1
    qte['cje'] = str(decimal.Decimal(qte['cje'][:-1]) * unit)

    # make result
    result = {"code": code, "quote": qte}

    return result
