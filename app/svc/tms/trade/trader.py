from tlib.stock import trade
from . import config


# trader default instance
default = trade.trades.Trades()


def setup():
    """
        setup default trader
    :return:
    """
    # add trade account
    for account in config.ACCOUNTS:
        default.add(account['id'], **account)