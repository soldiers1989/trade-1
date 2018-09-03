"""
    enum type for data
"""


class _Enum:
    def __init__(self, code, name):
        """
            init enum data with it's code and name
        :param code: str
        :param name: str
        """
        self.code = code
        self.name = name


class _PType:
    """
        trade price type
    """
    sj = _Enum('sj', '市价')
    xj = _Enum('xj', '限价')

ptype = _PType


class _TType:
    """
        trade order type
    """
    buy = _Enum('buy', '买入')
    sell = _Enum('sell', '卖出')
    close = _Enum('close', '平仓')

ttype = _TType


class _Order:
    """
        order status
    """
    notsend = _Enum('notsend', '未报')
    tosend = _Enum('tosend', '待报')
    sending = _Enum('sending', '正报')
    sent = _Enum('sent', '已报')
    tocancel = _Enum('tocancel', '待撤')
    canceling = _Enum('canceling', '待撤')
    pcanceled = _Enum('pcanceled', '部撤')
    tcanceled = _Enum('tcanceled', '已撤')
    fcanceled = _Enum('fcanceled', '撤废')
    pdeal = _Enum('pdeal', '部成')
    tdeal = _Enum('tdeal', '已成')
    dropped = _Enum('dropped', '废单')
    expired = _Enum('expired', '过期')

order = _Order


class _Trade:
    """
        trade status
    """
    tobuy = _Enum('tobuy', '待买')
    cancelbuy = _Enum('cancelbuy', '买撤')
    hold = _Enum('hold', '持仓')
    tosell = _Enum('tosell', '待卖')
    cancelsell = _Enum('cancelsell', '卖撤')
    sold = _Enum('sold', '已卖')
    toclose = _Enum('toclose', '待平')
    cancelclose = _Enum('cancelclose', '平撤')
    closed = _Enum('closed', '已平')
    canceled = _Enum('canceled', '已撤')
    expired = _Enum('expired', '过期')
    discard = _Enum('discard', '废单')

trade = _Trade


class _Coupon:
    """
        coupon status
    """
    used = _Enum('used', '已使用')
    unused = _Enum('unused', '未使用')

coupon = _Coupon


class _Stock:
    """
        stock status
    """
    open = _Enum('open', '正常')
    closed = _Enum('closed', '停牌')
    delisted = _Enum('delisted', '退市')

stock = _Stock


class _Risk:
    """
        stock risk control status
    """
    none = _Enum('none', '正常')
    nobuy = _Enum('nobuy', '禁买')
    nodelay = _Enum('nodelay', '禁延')

risk = _Risk


def values(enumcls):
    choices = []
    attrs = dir(enumcls)
    for name in attrs:
        attr = getattr(enumcls, name)
        if isinstance(attr, _Enum):
            choices.append(attr.code)
    return choices


if __name__ == '__main__':
    choices = values(risk)
    print(choices)