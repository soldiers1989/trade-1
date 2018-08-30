"""
    state machine for trade/order
"""


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

