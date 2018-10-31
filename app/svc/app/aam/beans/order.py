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


def list(**conds):
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
    results = dao.list(**conds)

    return results


def place(form: forms.order.Order):
    """
        place order
    :param form: obj, order
    :return:
    """
    # connect database
    db = mysql.get()

    # init dao object
    dao = daos.order.OrderDao(db)

    # prepare status log
    odate, otime = datetime.date.today(), int(time.time())
    logobj = [suite.status.order.format(form.operator, form.otype, form.optype, str(form.oprice), form.ocount, '', suite.enum.order.notsend.code, otime)]
    slog = suite.status.order.dumps(logobj)

    with dao.transaction():
        # add buy order
        nrows = dao.add(form.account, form.scode, form.sname, form.tcode, form.otype, form.optype, form.oprice, form.ocount, otime, odate, form.callback, slog)
        if nrows != 1:
            raise error.trade_order_add_failed

        # last add record id
        id = db.last_row_id()

        # get record
        order = dao.get(id=id)

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
        order = dao.get(id = form.id)
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
        logs.append(suite.status.order.format(form.operator, suite.enum.oaction.cancel.code, order.optype, str(order.oprice),
                                              order.ocount, order.status, nextstatus, time_now))
        slog = suite.status.trade.dumps(logs)

        # update data
        with dao.transaction():
            # update order
            dao.update(form.id, status=nextstatus, slog=slog)

            # get new record
            order = dao.get(id=form.id)

            # callback
            if order.status in [suite.enum.order.tcanceled.code] and order.callback is not None:
                service.asynchttp.post(order.callback, params=order, callback=_Callback())

            return order


def notify(form: forms.order.Notify):
    """
        order result notify
    :param form:
    :return:
    """
    # check form data
    if form.status in [suite.enum.order.notsend.code, suite.enum.order.tocancel.code]:
        raise error.trade_order_notify_denied

    # connect database
    db = mysql.get()

    # init dao object
    dao = daos.order.OrderDao(db)

    # lock order first
    with lock.order(form.id):
        # get order
        order = dao.get(id = form.id)
        if order is None:
            raise error.invalid_parameters

        # prepare status log
        logs = suite.status.trade.loads(order.slog)
        time_now = int(time.time())
        logs.append(suite.status.order.format(form.operator, suite.enum.oaction.notify.code, order.optype, str(order.oprice), order.ocount,order.status, form.status, time_now))
        slog = suite.status.trade.dumps(logs)

        # update data
        with dao.transaction():
            # update order
            if form.status in [suite.enum.order.tosend.code, suite.enum.order.sending.code, suite.enum.order.sent.code, suite.enum.order.canceling.code,
                               suite.enum.order.tcanceled.code, suite.enum.order.fcanceled.code, suite.enum.order.dropped.code, suite.enum.order.expired.code]:
                dao.update(form.id, status=form.status, slog=slog)
            elif form.status in [suite.enum.order.pcanceled.code, suite.enum.order.pdeal.code, suite.enum.order.tdeal.code]:
                dao.update(form.id, dcode=form.dcode, dcount=form.dcount, dprice=form.dprice, dtime=time_now, utime=time_now, status=form.status, slog=slog)
            else:
                raise error.trade_order_notify_denied

            # get new record
            order = dao.get(id=form.id)

            # callback
            service.asynchttp.post(order.callback, params=order, callback=_Callback())

            return order


def update(form: forms.order.Update):
    """
        update order
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
        order = dao.get(id = form.id)
        if order is None:
            raise error.invalid_parameters

        # prepare status log
        logs = suite.status.trade.loads(order.slog)
        time_now = int(time.time())
        logs.append(suite.status.order.format(form.operator, suite.enum.oaction.notify.code, order.optype, str(order.oprice), order.ocount,order.status, form.status, time_now))
        slog = suite.status.trade.dumps(logs)

        # update data
        with dao.transaction():
            # udpate column values
            cvals = {
                'status': form.status
            }
            if form.ocode is not None:
                cvals['ocode'] = form.ocode

            # update order
            dao.update(form.id, **cvals)

            # get new record
            order = dao.get(id=form.id)
            return order