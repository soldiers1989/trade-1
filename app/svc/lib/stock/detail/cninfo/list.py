"""
    get stock list
"""
import requests
from datetime import datetime, timedelta
from lib.stock.detail.cninfo import config


def _parse(record):
    """
        parse one record
    :param record:
    :return:
    """
    # alias for source to target
    alias = {
        "code": '证券代码', "name": '证券简称',
        "kpj": '开盘价', "spj": '收盘价', "zgj": '最高价', "zdj": '最低价',
        "cjl": '成交数量', "cje": '成交金额',
        "date": '交易日期'
    }

    result = {}
    # translate record by alias
    for key in alias.keys():
        result[key] = record[alias[key]]
        result['code'] = result['code'].split('-')[0]

    return result


def fetch():
    """
        fetch stock list
    :return:
    """
    results = []

    # get last date string
    lastday = (datetime.today()-timedelta(1)).strftime('%Y%m%d')

    # get each market data
    for market in config.MARKETS:
        # generate url
        url = config.URL % (market, lastday)

        # request data
        resp = requests.get(url, timeout=config.TIMEOUT, headers=config.HEADERS).json()

        # parse all response
        records = resp.get('records')

        # parse each record
        for record in records:
            # add to results
            results.append(_parse(record))

    return results


if __name__ == "__main__":
    records = fetch()
    for record in records:
        print(record)
