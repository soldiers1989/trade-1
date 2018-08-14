"""
    enum data definition
"""


# coupon status
class _Coupon:
    status = {
        'unused': '未用',
        'used': '已用'
    }

coupon = _Coupon


# trade order type/price/status
class _Order:
    type = {
        'buy': '买入',
        'sell': '卖出',
        'close': '平仓'
    }

    price = {
        'xj': '限价',
        'sj': '市价'
    }

    status = {
        'to': '待买入',
        'buying': '买入中',
    }


order = _Order
