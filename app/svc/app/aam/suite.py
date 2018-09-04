"""
    aam code suite
"""
import json


class _ItemTpl:
    def __init__(self, item, detail):
        self.item = item
        self.detail = detail


class _Tpl:
    """
        template for message
    """
    class _Bill:
        margin = _ItemTpl('保证金', '扣保证金%s元')

    bill = _Bill


    class _TradeMargin:
        init = _ItemTpl('初始保证金', '初始保证金%s元')
        add = _ItemTpl('追加保证金', '追加保证金%s元')

    trademargin = _TradeMargin

tpl = _Tpl


class _Status:
    @staticmethod
    def format(operator, action, before, after, time):
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
        return json.loads(jsonstr)

    @staticmethod
    def dumps(obj):
        """
            dump obj to json string
        :param obj:
        :return:
        """
        return json.dumps(obj)

status = _Status


class _Trade:
    # user trade state transition limit
    user = {
        'hold': ['tosell'],
    }

    # system trade state transition limit
    sys = {
        'tobuy': ['hold', 'expired', 'discard'],
        'hold': ['toclose'],
        'tosell': ['sold', 'hold'],
        'toclose': ['closed', 'hold']
    }

trade = _Trade


class _State:
    class _Order:
        # user trade order state transition limit
        user = {
            'notsend': ['tocancel'],
            'tosend': ['tocancel'],
            'sending': ['tocancel'],
            'sent': ['tocancel']
        }

        # system trade order state transition limit
        sys = {
            'notsend': ['tosend', 'sending', 'sent', 'pdeal', 'tdeal', 'dropped', 'expired'],
            'tosend': ['sending', 'sent', 'pdeal', 'tdeal', 'dropped', 'expired'],
            'sending': ['sent', 'pdeal', 'tdeal', 'dropped', 'expired'],
            'sent': ['pdeal', 'tdeal', 'dropped', 'expired'],
            'tocancel': ['canceling', 'pcanceled', 'tcanceled','fcanceled', 'expired'],
            'canceling': ['pcanceled', 'tcanceled', 'expired']
        }

    order = _Order

state = _State


class _Pair:
    def __init__(self, code, name):
        """
            init enum data with it's code and name
        :param code: str
        :param name: str
        """
        self.code = code
        self.name = name


class _Enum:
    class _Otype:
        """
            trade order type
        """
        buy = _Pair('buy', '买入')
        sell = _Pair('sell', '卖出')
        close = _Pair('close', '平仓')

    otype = _Otype

    class _PType:
        """
            trade price type
        """
        sj = _Pair('sj', '市价')
        xj = _Pair('xj', '限价')

    ptype = _PType

    class _Order:
        """
            order status
        """
        notsend = _Pair('notsend', '未报')
        tosend = _Pair('tosend', '待报')
        sending = _Pair('sending', '正报')
        sent = _Pair('sent', '已报')
        tocancel = _Pair('tocancel', '待撤')
        canceling = _Pair('canceling', '待撤')
        pcanceled = _Pair('pcanceled', '部撤')
        tcanceled = _Pair('tcanceled', '已撤')
        fcanceled = _Pair('fcanceled', '撤废')
        pdeal = _Pair('pdeal', '部成')
        tdeal = _Pair('tdeal', '已成')
        dropped = _Pair('dropped', '废单')
        expired = _Pair('expired', '过期')

    order = _Order

    class _Trade:
        """
            trade status
        """
        tobuy = _Pair('tobuy', '待买')
        cancelbuy = _Pair('cancelbuy', '买撤')
        hold = _Pair('hold', '持仓')
        tosell = _Pair('tosell', '待卖')
        cancelsell = _Pair('cancelsell', '卖撤')
        sold = _Pair('sold', '已卖')
        toclose = _Pair('toclose', '待平')
        cancelclose = _Pair('cancelclose', '平撤')
        closed = _Pair('closed', '已平')
        canceled = _Pair('canceled', '已撤')
        expired = _Pair('expired', '过期')
        discard = _Pair('discard', '废单')

    trade = _Trade

    class _Coupon:
        """
            coupon status
        """
        used = _Pair('used', '已使用')
        unused = _Pair('unused', '未使用')

    coupon = _Coupon

    class _Stock:
        """
            stock status
        """
        open = _Pair('open', '正常')
        closed = _Pair('closed', '停牌')
        delisted = _Pair('delisted', '退市')

    stock = _Stock

    class _Risk:
        """
            stock risk control status
        """
        none = _Pair('none', '正常')
        nobuy = _Pair('nobuy', '禁买')
        nodelay = _Pair('nodelay', '禁延')

    risk = _Risk

    class _Operator:
        """
            operator for trade command
        """
        sys = _Pair('sys', '系统')
        user = _Pair('user', '用户')
        trader = _Pair('trade', '交易员')

    operator = _Operator

    def values(enumcls):
        choices = []
        attrs = dir(enumcls)
        for name in attrs:
            attr = getattr(enumcls, name)
            if isinstance(attr, _Pair):
                choices.append(attr.code)
        return choices

enum = _Enum
