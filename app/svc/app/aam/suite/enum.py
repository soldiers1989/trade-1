"""
    enum value definition
"""


class _Pair:
    def __init__(self, code, name):
        """
            init enum data with it's code and name
        :param code: str
        :param name: str
        """
        self.code = code
        self.name = name


class _OAction:
    """
        order action
    """
    buy = _Pair('buy', '买入')
    sell = _Pair('sell', '卖出')
    close = _Pair('close', '平仓')
    cancel = _Pair('cancel', '撤销')
    drop = _Pair('drop', '弃单')
    notify = _Pair('notify', '回报')

oaction = _OAction


class _OType:
    """
        trade order type
    """
    buy = _Pair('buy', '买入')
    sell = _Pair('sell', '卖出')

otype = _OType


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
    canceling = _Pair('canceling', '正撤')
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
    buying = _Pair('buying', '正买')
    cancelbuy = _Pair('cancelbuy', '撤买')
    buycanceling = _Pair('buycanceling', '正撤买')

    canceled = _Pair('canceled', '已撤')

    hold = _Pair('hold', '持仓')

    tosell = _Pair('tosell', '待卖')
    selling = _Pair('selling', '正卖')
    cancelsell = _Pair('cancelsell', '撤卖')
    sellcanceling = _Pair('sellcanceling', '正撤卖')

    sold = _Pair('sold', '已卖')

    toclose = _Pair('toclose', '待平')
    closing = _Pair('closing', '正平')
    cancelclose = _Pair('cancelclose', '撤平')
    closecanceling = _Pair('closecanceling', '正撤平')

    closed = _Pair('closed', '已平')

    expired = _Pair('expired', '过期')

    dropped = _Pair('dropped', '废单')

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
    """
        get enum values from enum class
    :param enumcls:
    :return:
    """
    choices = []
    attrs = dir(enumcls)
    for name in attrs:
        attr = getattr(enumcls, name)
        if isinstance(attr, _Pair):
            choices.append(attr.code)
    return choices
