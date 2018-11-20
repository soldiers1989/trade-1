"""
    risk management
"""
import threading


class _RiskManager:
    """
        manage warning & stop loss trade, trade struct:
        'warn'->trade list
        'loss'->trade list
    """
    def __init__(self):
        # type->trade list
        self._trades = {}
        # lock for trades
        self._lock = threading.RLock()

    def set(self, type, trades):
        """
            set risk trades
        :param type: str, 'warning' for warning trades or 'stoploss' for stop loss trades or 'normal' for normal trades
        :param trades: list, user trade list which each record is dict
        :return:
            None
        """
        with self._lock:
            self._trades[type] = trades

    def get(self, type=None):
        """
            get trade list by type
        :param type: str, 'warning' or 'stoploss' or 'normal'
        :return:
            trade list
        """
        with self._lock:
            if type is not None:
                return self._trades.get(type, [])
            trades = []
            for lst in self._trades.values():
                trades.extend(lst)
            return trades


# risk manager object
_riskmanager = _RiskManager()


def set(type, trades):
    """
        set risk trades
    :param type: str, 'warning' for warning trades or 'stoploss' for stop loss trades or 'normal' for normal trades
    :param trades: list, user trade list which each record is dict
    :return:
        None
    """
    _riskmanager.set(type, trades)


def get(type=None):
    """
        get trade list by type
    :param type: str, 'warning' or 'stoploss' or 'normal
    :return:
        trade list
    """
    return _riskmanager.get(type)
