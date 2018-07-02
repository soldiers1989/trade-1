"""
    parser for ifeng quote response
"""
import json, time, math, decimal


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
            quote[p] = quote[p] #str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

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
    # parse results
    results = []

    # alias for item
    alias = {
        "jkj": 4, "zsj": 1, "dqj": 0, "zgj": 5, "zdj": 6,
        "cjl": 9, "cje": 10,
        "mrl1": 16, "mrj1": 11, "mrl2": 17, "mrj2": 12, "mrl3": 18, "mrj3": 13, "mrl4": 19, "mrj4": 14, "mrl5": 20, "mrj5": 15,
        "mcl1": 26, "mcj1": 21, "mcl2": 27, "mcj2": 22, "mcl3": 28, "mcj3": 23, "mcl4": 29, "mcj4": 24, "mcl5": 30, "mcj5": 25,
        "time": 34,
    }

    # parse all response quotes
    rpos = text.find('=') + 1
    text = text[rpos:].rstrip().rstrip(';')
    quotes = json.loads(text)

    # parse each quote
    for stock in quotes:
        # stock code
        code = stock[-6:]

        # quote items
        items = quotes[stock]

        qte = {}
        # stock quote
        for k in alias:
            qte[k] = items[alias[k]]

        # translate time from unix timestamp to datetime
        qte['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(qte['time']))

        # tidy quote
        qte = tidy(qte)

        # compute ztj&dtj
        qte['ztj'] = round(qte['zsj'] * 1.1, 2)
        qte['dtj'] = round(qte['zsj'] * 0.9, 2)

        # add to results
        results.append({'code': code, 'quote': qte})

    return results
