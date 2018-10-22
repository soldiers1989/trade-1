from . import config, broker


# trader default instance
default = broker.trades.Trades()


def setup():
    """
        setup default trader
    :return:
    """
    # add trade account
    for account in config.ACCOUNTS:
        default.add(account['id'], **account)
