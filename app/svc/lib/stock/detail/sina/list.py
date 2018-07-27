"""
    get stock list
"""
import time, requests
from lib.stock.detail.sina import config


def _tojson(text):
    """
    解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
    :param expr:非标准JSON的Javascript字符串
    :return:Python字典
    """
    obj = eval(text, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj


def _parse(record):
    """
        parse one record
    :param record:
    :return:
    """
    # alias for source to target
    alias = {
        'code':'code', 'name':'name',
        'dqj':'trade', 'mrj1':'buy', 'mcj1':'sell',
        'zsj':'settlement', 'jkj':'open', 'zgj':'high', 'zdj':'low',
        'cjl':'volume', 'cje':'amount',
        'zde':'pricechange', 'zdf':'changepercent',
        'tm':'ticktime'
    }

    result = {}
    # translate record by alias
    for key in alias.keys():
        result[key] = record[alias[key]]

    return result


def fetch():
    """
        fetch stock list
    :return:
    """
    results = []

    page = 1
    while page < config.MAX_PAGES:
        # generate current page url
        pageurl = config.URL % page

        # request page data
        resp = requests.get(pageurl, timeout=config.TIMEOUT, headers=config.HEADERS)

        # translate to json object
        records = _tojson(resp.text)
        if records == 'null':
            break;

        # parse records
        for record in records:
            results.append(_parse(record))

        # sleep for a while
        time.sleep(config.INTERVAL)

        # fetch next page
        page = page + 1

    return results


if __name__ == "__main__":
    a = _tojson('null')

    records = fetch()
    for record in records:
        print(record)
