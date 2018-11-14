"""
    order management
"""
import json,time, datetime, logging
from .. import access, handler, forms, protocol, trade, models, status, error, locker


class ListHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get account order list
        :return:
        """
        # list conditions
        conds = self.cleaned_arguments

        with models.db.create() as d:
            # get trade records
            orders = models.AccountOrder.filter(d, **conds).all()

            # remote slog field
            for order in orders:
                del order['slog']

            # success
            self.write(protocol.success(data=orders))


class PlaceHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order place
        :return:
        """
        # get form arguments
        form = forms.order.Place(**self.cleaned_arguments)

        # check order count/price
        trade.valid(form.scode, form.optype, form.oprice, form.ocount)

        with models.db.atomic() as d:
            # check if order has exist
            order = models.AccountOrder.filter(d, tcode=form.ocode).one()

            # add new order
            if order is None:
                # detail
                detail = '%s,%s,%s,%s,%s,%s' % (form.otype, form.optype, form.oprice, form.ocount, '0.0', '0')
                # status log
                slog = status.append(form.operator, form.otype, '', 'notsend', detail)

                # add order
                order = models.AccountOrder(tcode=form.ocode, account=form.account, scode=form.scode, sname=form.sname,
                                          otype=form.otype, optype=form.optype, oprice=form.oprice, ocount=form.ocount,
                                          odate=datetime.date.today(), otime=int(time.time()),
                                          dprice=0.0, dcount=0, status='notsend', slog=slog,
                                          ctime=int(time.time()), mtime=int(time.time())).save(d)

            # response
            self.write(protocol.success(data=order))


class CancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order cancel
        :return:
        """
        # get arguments
        form = forms.order.Cancel(**self.arguments)

        with models.db.atomic() as d, locker.order(form.id):
            # filters
            filters = {}
            if form.id is not None:
                filters['id'] = form.id
            if form.ocode is not None:
                filters['tcode'] = form.ocode

            # get order object
            order = models.AccountOrder.filter(d, **filters).one()
            if order is None:
                raise error.order_not_exist

            # check current order status
            if order.status not in ['notsend', 'tosend', 'sending', 'sent']:
                raise error.order_operation_denied

            # next status
            nextstatus = 'tcanceled' if order.status in ['notsend'] else 'tocancel'

            #status log
            detail = '%s,%s,%s,%s,%s,%s' % (order.otype, order.optype, order.oprice, order.ocount, order.dprice, order.dcount)
            order.slog = status.append(form.operator, 'cancel', order.status, nextstatus, detail, order.slog)

            # update order
            order.save(d)

            # response
            self.write(protocol.success(data=order))


class NotifyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order notify, post data format:
            [
                {account:account, ocode:ocode, dprice:dprice, dcount:dcount, status:status, operator:operator},
                {account:account, ocode:ocode, dprice:dprice, dcount:dcount, status:status, operator:operator},
                ......
            ]
        :return:
        """
        # get notify orders
        notifyorders = json.loads(self.request.body.decode())

        # validate notify orders
        for notifyorder in notifyorders:
            if not {'account','ocode','dprice','dcount','status','operator'}.issubset(set(notifyorder.keys())):
                raise error.order_notify_data_invalid
            if notifyorder['status'] not in ['sent','canceling','pcanceled','tcanceled','fcanceled','pdeal','tdeal','dropped']:
                raise error.order_notify_data_invalid

        with models.db.atomic() as d:
            # get all pending orders of today
            localorders = models.AccountOrder.filter(d, odate=datetime.date.today(), ocode__null=True, status__in=('notsend, tosend, sending, sent, tocancel, canceling, pdeal')).all()

            # updated orders
            updatedorders = []

            # process each order
            for notifyorder in notifyorders:
                for localorder in localorders:
                    if notifyorder['account']==localorder.account and notifyorder['ocode']==localorder.ocode:
                        try:
                            with locker.order(localorder.id):
                                # status log
                                detail = '%s,%s,%s,%s,%s,%s' % (localorder.otype, localorder.optype, localorder.oprice, localorder.ocount, notifyorder['dprice'], notifyorder['dcount'])
                                slog = status.append(notifyorder['operator'], 'notify', localorder.status, notifyorder['status'], detail, localorder.slog)

                                #update trade order
                                localorder.update(dprice=notifyorder['dprice'],
                                                 dcount=notifyorder['dcount'],
                                                 status=notifyorder['status'],
                                                 slog=slog,
                                                 ddate=datetime.date.today(),
                                                 dtime=int(time.time()),
                                                 mtime=int(time.time()))
                                localorder.save(d)

                                updatedorders.append(localorder)
                        except Exception as e:
                            logging.error('notify: %s->%s, error: %s' % (str(localorder), str(notifyorder), str(e)))


            # response data
            data = {
                'updated': len(updatedorders),
                'updates': updatedorders
            }
            self.write(protocol.success(data=data))


class OCodeHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order code notify
        :return:
        """
        # get form arguments
        form = forms.order.OCode(**self.cleaned_arguments)

        with models.db.atomic() as d, locker.order(form.id):
            # udpate order code
            models.AccountOrder.filter(d, id=form.id).update(ocode=form.ocode)

            self.write(protocol.success())
