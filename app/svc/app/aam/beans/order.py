"""
    trade order operations
"""
import time, datetime, logging
from tlib import chttp
from .. import suite, daos, error, lock, mysql, forms, service


class _Callback(chttp.Callback):
    """
        order callback
    """
    def on_succeed(self, req, resp):
        """
            request success call back
        :param req: obj, request object
        :param resp: obj, request response object
        :return:
        """
        logging.info('callback: %s, succeed' % req.url)

    def on_failed(self, req, error):
        """
            request failed call back
        :param req: obj, request object
        :param error: str, request failed message
        :return:
        """
        logging.info('callback: %s, failed, error: %s' % (req.url, error))


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


def buy(form: forms.order.Buy):
    """
        buy order
    :param form:
    :return:
    """
    # connect database
    db = mysql.get()

    # init dao object
    dao = daos.order.OrderDao(db)

    # prepare status log
    odate, otime = datetime.date.today(), int(time.time())
    logobj = [suite.status.order.format(form.operator, suite.enum.oaction.buy.code, form.optype, str(form.oprice), form.ocount, '', suite.enum.order.notsend.name, otime)]
    slog = suite.status.order.dumps(logobj)

    with dao.transaction():
        # add buy order
        nrows = dao.add_order(form.account, form.scode, form.sname, form.tcode, suite.enum.otype.buy.code, form.optype, form.oprice, form.ocount, otime, odate, form.callback, slog)
        if nrows != 1:
            raise error.trade_order_add_failed

        # last add record id
        id = db.lastrowid()

        # get record
        order = dao.get_order(id=id)

        return order


def sell(form: forms.order.Sell):
    """
        sell order
    :param form:
    :return:
    """
    # connect database
    db = mysql.get()

    # init dao object
    dao = daos.order.OrderDao(db)

    # prepare status log
    odate, otime = datetime.date.today(), int(time.time())
    logobj = [suite.status.order.format(form.operator, suite.enum.oaction.sell.code, form.ptype, str(form.oprice), form.ocount, '', suite.enum.order.notsend.name, otime)]
    slog = suite.status.order.dumps(logobj)

    with dao.transaction():
        # add buy order
        nrows = dao.add_order(form.account, form.scode, form.sname, form.tcode, suite.enum.otype.sell.code, form.optype, form.oprice, form.ocount, otime, odate, form.callback, slog)
        if nrows != 1:
            raise error.trade_order_add_failed

        # last add record id
        id = db.lastrowid()

        # get record
        order = dao.get_order(id=id)

        return order


def cancel(form: forms.order.Cancel):
    """
        cancel order
    :param form:
    :return:
    """
    # connect database
    db = mysql.get()

    # init dao object
    dao = daos.order.OrderDao(db)

    # lock order first
    with lock.order(form.id):
        # get order
        order = dao.get_order(id = form.id)
        if order is None:
            raise error.invalid_parameters

        # check current order status
        if order.status not in [suite.enum.order.notsend.code, suite.enum.order.tosend.code, suite.enum.order.sending.code,
                                suite.enum.order.sent.code]:
            raise error.trade_operation_denied

        # next status
        if order.status in [suite.enum.order.notsend.code]:
            nextstatus = suite.enum.order.tcanceled.code
        else:
            nextstatus = suite.enum.order.tocancel.code

        # prepare status log
        logs = suite.status.trade.loads(order.slog)
        time_now = int(time.time())
        logs.append(suite.status.order.format(form.operator,
                                              suite.enum.oaction.cancel.code,
                                              order.optype,
                                              str(order.oprice),
                                              order.ocount,
                                              order.status,
                                              nextstatus,
                                              time_now))
        slog = suite.status.trade.dumps(logs)

        # update data
        with dao.transaction():
            # update order
            dao.update_order(form.id, status=nextstatus, slog=slog)

            # get new record
            order = dao.get_order(id=form.id)

            # callback
            if order.status in [suite.enum.order.tcanceled.code] and order.callback is not None:
                service.asynchttp.post(order.callback, params=order, callback=_Callback())

            return order


def bought(form: forms.order.Bought):
    """
       order has been bought
    :param form:
    :return:
    """
    pass


def sold(form: forms.order.Sold):
    """
        order has been sold
    :param form:
    :return:
    """
    pass


def canceled(form: forms.order.Canceled):
    """
        order has been canceled
    :param form:
    :return:
    """
    pass


def notify(form: forms.order.Notify):
    """
        order result notify
    :param form:
    :return:
    """