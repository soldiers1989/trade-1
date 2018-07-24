"""
    parse response
"""
import math
from lib.stock.quote.daily import error


def parse(resp):
    """
        parse response json object
    :param resp: obj
    :return:
    """
    try:
        # parse results
        results = []

        # alias for item
        alias = {
            "code": '证券代码', "name": '证券简称',
            "kpj": '开盘价', "spj": '收盘价', "zgj": '最高价', "zdj": '最低价',
            "cjl": '成交数量', "cje": '成交金额',
            "date": '交易日期'
        }

        # parse all response quotes
        records = resp.get('records')

        # parse each quote
        for record in records:
            # quote
            quote = {}

            # process item
            for k in alias:
                quote[k] = record[alias[k]]

            # process stock code
            quote['code'] = quote['code'].split('-')[0]

            # add to results
            results.append(quote)

        return results
    except Exception as e:
        raise error.ParseError(str(e))
