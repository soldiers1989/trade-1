"""
    stock market data
"""
import logging
from .. import src


class StockApi:
    def __init__(self):
        pass

    def get(self, type, callback=None, format=None, **kwargs):
        """
            查询指定数据类型的数据，如果callback不为None则为异步查询, 查询结果将通过回调函数返回

            # 回调函数：
                callback(status, message, data)
            # 数据类型：
                * list
                    查询当前所有上市的股票列表
                * ticks
                    查询指定股票和日期的逐笔委托记录，参数
                    * zqdm: 证券代码
                    * date* 交易日期

        :param type: str, 数据类型
        :param callback: function, 异步请求回调函数
        :param format: str, 结果数据格式, pandas.DataFrame or basic types list/dict/...
        :param kwargs: dict, 其它参数
        :return:
            None or data
        """
        pass

    def sub(self, type, callback, format=None, **kwargs):
        """
            订阅指定数据类型的数据
            # 回调函数：
                callback(status, message, data)
            # 数据类型：
                * ticks
                    逐笔委托
                * level5
                    查询指定股票和日期的逐笔委托记录，参数
                    * zqdm: 证券代码
                    * date* 交易日期
        :param type:
        :param callback:
        :param format:
        :param kwargs:
        :return:
        """
        pass
