"""
    get stock list
"""
import requests
from datetime import datetime, timedelta
from . import config


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


def _last_trading_day():
    """
        get last trading day
    :return:
    """
    last_trading_day = datetime.today()

    # skip weekend
    if last_trading_day.isoweekday() == 7:
        last_trading_day = last_trading_day - timedelta(2)
    elif last_trading_day.isoweekday() == 6:
        last_trading_day = last_trading_day - timedelta(1)
    else:
        pass

    # skip holidays
    while last_trading_day.strftime('%Y-%m-%d') in config.HOLIDAYS:
        last_trading_day = last_trading_day - timedelta(1)

    #last trading day
    return last_trading_day


def fetch():
    """
        fetch stock list
    :return:
    """
    results = []

    # get last date string
    lastday = _last_trading_day().strftime('%Y-%m-%d')

    # get each market data
    for market in config.MARKETS:
        # generate url
        url = config.URL % (market, lastday)

        # request data
        resp = requests.get(url, timeout=config.TIMEOUT, headers=config.HEADERS).json()

        # parse all response
        records = resp.get('records')

        # parse each record
        if records is not None:
            for record in records:
                # add to results
                results.append(_parse(record))

    return results


if __name__ == "__main__":
    records = fetch()
    for record in records:
        print(record)
