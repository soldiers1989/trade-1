"""
    stock data
"""
from . import client
from .. import util


class _KData:
    def __init__(self):
        pass

    def get(self, **kwargs):
        """
            获取K线数据
        :param kwargs:
                zqdm: 证券代码
                type: d-日线, w-周, m-月, 5-5分钟, 15-15分钟, 30-30分钟, 60-60分钟
        :return:
            list, 格式:
            [{time:时间, kpj:开盘价, spj: 收盘价, zgj: 最高价, zdj: 最低价, zde: 涨跌额, zdf: 涨跌幅, cjl: 成交量, hsl: 换手率}, ... ]

        """
        # url templates
        urltpls = {
            'd': '/akdaily/?code=%s&type=last',
            'w': '/akweekly/?code=%s&type=last',
            'm': '/akmonthly/?code=%s&type=last',
            '5': '/akmin?scode=%s&type=5',
            '15': '/akmin?scode=%s&type=15',
            '30': '/akmin?scode=%s&type=30',
            '60': '/akmin?scode=%s&type=60'
        }

        # get parameters
        zqdm, type = kwargs.get('zqdm'), kwargs.get('type')
        if zqdm is None or type is None:
            raise ValueError('parameters zqdm and type must not be none')
        zqdm, type = util.addse(zqdm), type.lower()
        if type not in urltpls.keys():
            raise ValueError('k-data type %s not support in <d, w, m, 5, 15, 30, 60>' % type)

        # request path
        path = urltpls[type] % zqdm

        # request data
        resp = client.apifinance.get(path)

        # parse data
        results = self._parse(resp.text)

        return results

    def _parse(self, text):
        """
            解析每条数据记录
        :param record:
        :return:
        """
        # convert text
        objs = util.json(text)

        # get records
        records = objs['record']

        results = []
        # parse each records
        for record in records:
            results.append({
                'time': record[0],
                'kpj': record[1],
                'spj': record[3],
                'zgj': record[2],
                'zdj': record[4],
                'zde': record[6],
                'zdf': record[7],
                'cjl': record[5],
                'hsl': None if len(record)<15 else record[14]
            })

        return results

kdata = _KData()