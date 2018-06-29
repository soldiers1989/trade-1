from lib.stock import trade
from app.trade import config


def create():
    """
        trader for trade service
    """
    # create trades
    trades = trade.trades.Trades()

    # add trade account
    for acnt in config.ACCOUNTS:
        # create account
        acount = trade.tdx.account.Account(*acnt)

        # add account
        id = acnt[0]
        trades.add(id, acount)

    return trades

# trader default instance
default = create()
