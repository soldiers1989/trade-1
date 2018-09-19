"""
    status transform formatter
"""
import json


class _Trade:
    @staticmethod
    def format(operator, action, ptype, price, count, before, after, time):
        """
            format an new  status chagne record
        :param operator:
        :param action:
        :param before:
        :param after:
        :param time:
        :return:
        """
        return {
            'user': operator,
            'action': action,
            'ptype': ptype,
            'price': price,
            'count': count,
            'before': before,
            'after': after,
            'time': time
        }

    @staticmethod
    def loads(jsonstr):
        """
            load a json string to obj
        :param jsonstr:
        :return:
        """
        if jsonstr is None:
            return []
        return json.loads(jsonstr)

    @staticmethod
    def dumps(obj):
        """
            dump obj to json string
        :param obj:
        :return:
        """
        if obj is None:
            return '[]'

        return json.dumps(obj)

trade = _Trade
order = _Trade
