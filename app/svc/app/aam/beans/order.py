"""
    trade order operations
"""
from .. import suite, daos, error, lock, trade, mysql, forms


def get_orders(**conds):
    """
        get order records
    :param conds:
    :return:
    """
    # connect database
    db = mysql.get()

    # init dao object
    dao = daos.order.OrderDao(db)

    # get records
    results = dao.get_orders(**conds)

    return results


def buy(form):
    """
        buy order
    :param form:
    :return:
    """
    pass


def sell(form):
    """
        sell order
    :param form:
    :return:
    """
    pass


def cancel(form):
    """
        cancel order
    :param form:
    :return:
    """
    pass


def bought(form):
    """
       order has been bought
    :param form:
    :return:
    """
    pass


def sold(form):
    """
        order has been sold
    :param form:
    :return:
    """
    pass


def canceled(form):
    """
        order has been canceled
    :param form:
    :return:
    """
    pass
