"""
    enum data definition
"""


# all enum data for class
all = {
    # common enum
    'common': {
        'enable': {
            True: '启用',
            False: '禁用'
        },
        'disable': {
            True: '禁用',
            False: '启用'
        },
        'deleted': {
            True: '已删除',
            False: '未删除'
        }
    },

    # charge status
    'charge': {
        'status': {
            'topay': '待付款',
            'paid': '已付款',
            'expired': '已失效'
        }
    },

    # draw status
    'draw': {
        'status': {
            'topay': '待付款',
            'paid': '已付款',
            'denied': '已拒绝'
        }
    },

    # coupon type/status
    'coupon': {
        'type': {
            'cash': '现金',
            'discount': '打折'
        },
        'status': {
            'notused': '未用',
            'used': '已用',
            'expired': '过期'
        }
    },

    # trade order type/price/status
    'order': {
        'type': {
            'buy': '买入',
            'sell': '卖出',
            'close': '平仓'
        },

        'price': {
            'xj': '限价',
            'sj': '市价'
        },

        'status': {
            'notsend': '未报',
            'tosend': '待报',
            'sending': '正报',
            'sent': '已报',
            'tocancel':'待撤',
            'canceling':'正撤',
            'pcanceled':'部撤',
            'tcanceled':'已撤',
            'fcanceled':'撤废',
            'pdeal':'部成',
            'tdeal':'已成',
            'dropped':'废单',
            'expired': '过期'
        }
    },

    # user trade status
    'trade': {
        'status': {
            'tobuy': '待买',
            'buying': '正买',
            'cancelbuy': '撤买',
            'buycanceling': '买撤',
            'canceled': '已撤',
            'hold': '持仓',
            'tosell': '待卖',
            'selling': '正卖',
            'cancelsell': '撤卖',
            'sellcanceling': '卖撤',
            'sold': '已卖',
            'toclose': '待平',
            'closing': '正平',
            'cancelclose': '撤平',
            'closecanceling': '平撤',
            'closed': '已平',
            'expired': '过期',
            'dropped': '废单'
        }
    },

    # stock status/limit
    'stock': {
        'status': {
            'open': '正常',
            'close': '停牌',
            'delisted': '退市'
        },

        'limit': {
            'none': '正常',
            'nobuy': '禁买',
            'nodelay': '禁延'
        }
    }
}
