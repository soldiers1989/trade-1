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
            quote[p] = quote[p] #str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

    # tidy volumes
    for v in volumes:
        if quote.get(v) is not None:
            quote[v] = int(quote[v])

    return quote


def parse(jsonobj):
    """
        parse response text
    :param text:
    :return:
    """
    # parse results
    results = []

    # alias for item
    alias = {
        "jkj": 'openPrice', "zsj": 'preClosePrice', "dqj": 'lastPrice', "zgj": 'highPrice', "zdj": 'lowPrice',
        "cjl": 'volume', "cje": 'amount',
        "mrl1": 'bidVolume1', "mrj1": 'bidPrice1', "mrl2": 'bidVolume2', "mrj2": 'bidPrice2', "mrl3": 'bidVolume3', "mrj3": 'bidPrice3', "mrl4": 'bidVolume4', "mrj4": 'bidPrice4', "mrl5": 'bidVolume5', "mrj5": 'bidPrice5',
        "mcl1": 'askVolume1', "mcj1": 'askPrice1', "mcl2": 'askVolume2', "mcj2": 'askPrice2', "mcl3": 'askVolume3', "mcj3": 'askPrice3', "mcl4": 'askVolume4', "mcj4": 'askPrice4', "mcl5": 'askVolume5', "mcj5": 'askPrice5',
        "time": 'lastModifyTime',
    }

    # quote items
    items = jsonobj['info']['result']
    # stock code
    code = items['stockCode']

    qte = {}
    # stock quote
    for k in alias:
        qte[k] = items[alias[k]]

    # transfer volume
    qte['cjl'] = math.floor(qte['cjl']/100)

    # tidy quote
    qte = tidy(qte)

    # compute ztj&dtj
    qte['ztj'] = round(qte['zsj']*1.1, 2)
    qte['dtj'] = round(qte['zsj']*0.9, 2)

    # make result
    result = {"code": code, "quote": qte}

    return result
