"""
    state transform definition
"""


class _Trade:
    # trade state transition limit by user
    user = {
        'tobuy': ['cancelbuy'],
        'hold': ['tosell'],
        'tosell': ['cancelsell']
    }

    # trade state transition limit buy system
    sys = {
        'tobuy': ['hold', 'expired', 'discard'],
        'cancelbuy': ['hold', 'canceled'],
        'hold': ['toclose'],
        'tosell': ['sold', 'hold'],
        'cancelsell': ['hold', 'sold'],
        'toclose': ['closed', 'hold']
    }

    # trade state transition limit buy trader
    trader = sys

    all = {'user': user, 'sys': sys, 'trader': trader}

trade = _Trade


class _Order:
    # trade order state transition limit by system
    user = {
        'notsend': ['tocancel'],
        'tosend': ['tocancel'],
        'sending': ['tocancel'],
        'sent': ['tocancel']
    }

    # trade order state transition limit by system
    sys = {
        'notsend': ['tosend', 'sending', 'sent', 'pdeal', 'tdeal', 'dropped', 'expired'],
        'tosend': ['sending', 'sent', 'pdeal', 'tdeal', 'dropped', 'expired'],
        'sending': ['sent', 'pdeal', 'tdeal', 'dropped', 'expired'],
        'sent': ['pdeal', 'tdeal', 'dropped', 'expired'],
        'tocancel': ['canceling', 'pcanceled', 'tcanceled','fcanceled', 'expired'],
        'canceling': ['pcanceled', 'tcanceled', 'expired']
    }

    # trade order state transition limit buy trader
    trader = sys

    all = {'user': user, 'sys': sys, 'trader': trader}

order = _Order
