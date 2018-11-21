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


class AccountsHandler(handler.Handler):
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

            # distinct accounts
            accounts = list(set([order['account'] for order in orders]))

            # success
            self.write(protocol.success(data=accounts))


class UpdateHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.order.Update(**self.cleaned_arguments)

        # get update items
        updateitems = {}
        for k in self.cleaned_arguments:
            updateitems[k] = form[k]

        with models.db.atomic() as d:
            # get account order object
            accountorder = models.AccountOrder.filter(d, id=form.id).one()
            if accountorder is None:
                raise error.order_not_exist

            # lock order
            with locker.order(accountorder.id):
                # update order
                orderprestatus = accountorder.status
                accountorder.update(**updateitems)
                detail = status.order_detail(**accountorder)
                accountorder.slog = status.append('sys', 'update', orderprestatus, accountorder.status, detail, accountorder.slog)
                accountorder.save(d)

                # response data
                self.write(protocol.success(data=accountorder))


class TakeHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            take today's not-send order, make to-send status
        :return:
        """
        with models.db.create() as d:
            # get account orders
            accountorders = models.AccountOrder.filter(d, status='notsend', odate=datetime.date.today()).all()

            taked, failed = [], []
            # take each order
            for accountorder in accountorders:
                try:
                    with locker.order(accountorder.id):
                        orderprestatus = accountorder.status
                        accountorder.status = 'tosend'
                        detail = status.order_detail(**accountorder)
                        accountorder.slog = status.append('sys', 'take', orderprestatus, accountorder.status, detail, accountorder.slog)
                        accountorder.save(d)
                        d.commit()

                        del accountorder['slog']
                        taked.append(accountorder)
                except Exception as e:
                    del accountorder['slog']
                    failed.append(accountorder)


            # response data
            data = {
                'taked': taked,
                'failed': failed
            }

            # success
            self.write(protocol.success(data=data))


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
                # status log
                detail = status.order_detail(**form)
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

            # update order
            orderprestatus = order.status
            order.status = 'tcanceled' if orderprestatus in ['notsend', 'tosend'] else 'tocancel'
            detail = status.order_detail(**order)
            order.slog = status.append(form.operator, 'cancel', orderprestatus, order.status, detail, order.slog)

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

        with models.db.create() as d:
            # get all pending orders of today
            localorders = models.AccountOrder.filter(d, odate=datetime.date.today(), status__in=('sent', 'tocancel', 'canceling', 'pdeal')).all()

            notified, failed = [], []
            # process each order
            for localorder in localorders:
                for notifyorder in notifyorders:
                    try:
                        if notifyorder['account']==localorder.account and notifyorder['ocode']==localorder.ocode:
                            with locker.order(localorder.id):
                                orderprestatus = localorder.status
                                #update trade order
                                localorder.update(dprice=notifyorder['dprice'],
                                                 dcount=notifyorder['dcount'],
                                                 status=notifyorder['status'],
                                                 ddate=datetime.date.today(),
                                                 dtime=int(time.time()),
                                                 mtime=int(time.time()))
                                detail = status.order_detail(**localorder)
                                localorder.slog = status.append(notifyorder.get('operator', 'sys'), 'notify', orderprestatus, localorder.status, detail, localorder.slog)

                                localorder.save(d)
                                d.commit()

                                del localorder['slog']
                                notified.append(localorder)
                    except Exception as e:
                        del localorder['slog']
                        notified.append(localorder)

            # response data
            data = {
                'notified': notified,
                'failed': failed
            }
            self.write(protocol.success(data=data))


class SendingHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order code notify
        :return:
        """
        # get form arguments
        form = forms.order.Sending(**self.cleaned_arguments)

        with models.db.atomic() as d, locker.order(form.id):
            # get order
            order = models.AccountOrder.filter(d, id=form.id).one()
            if order is None:
                raise error.order_not_exist
            if order.status not in ['tosend']:
                raise error.order_operation_denied

            # udpate order
            orderprestatus = order.status
            order.status = 'sending'
            detail = status.order_detail(**order)
            order.slog = status.append(form.operator, 'send', orderprestatus, order.status, detail, order.slog)

            order.save(d)

            del order['slog']
            self.write(protocol.success(data=order))


class SentHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order code notify
        :return:
        """
        # get form arguments
        form = forms.order.Sent(**self.cleaned_arguments)

        with models.db.atomic() as d, locker.order(form.id):
            # get order
            order = models.AccountOrder.filter(d, id=form.id).one()
            if order is None:
                raise error.order_not_exist
            if order.status not in ['sending']:
                raise error.order_operation_denied

            # udpate order
            orderprestatus = order.status
            order.status = 'sent'
            order.ocode = form.ocode
            detail = status.order_detail(**order)
            order.slog = status.append(form.operator, 'send', orderprestatus, order.status, detail, order.slog)

            order.save(d)

            del order['slog']
            self.write(protocol.success(data=order))


class DealtHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            notify order dealt
        :return:
        """
        # get form arguments
        form = forms.order.Dealt(**self.cleaned_arguments)

        with models.db.atomic() as d, locker.order(form.id):
            # get order
            order = models.AccountOrder.filter(d, id=form.id).one()
            if order is None:
                raise error.order_not_exist
            if order.status not in ['sent', 'tocancel', 'canceling']:
                raise error.order_operation_denied

            # udpate order
            orderprestatus = order.status
            order.status = 'pdeal' if form.dcount < order.ocount else 'tdeal'
            order.dprice = form.dprice
            order.dcount = form.dcount
            detail = status.order_detail(**order)
            order.slog = status.append(form.operator, 'deal', orderprestatus, order.status, detail, order.slog)

            order.save(d)

            del order['slog']
            self.write(protocol.success(data=order))


class CancelingHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            notify order canceling
        :return:
        """
        # get form arguments
        form = forms.order.Canceling(**self.cleaned_arguments)

        with models.db.atomic() as d, locker.order(form.id):
            # get order
            order = models.AccountOrder.filter(d, id=form.id).one()
            if order is None:
                raise error.order_not_exist
            if order.status not in ['tocancel']:
                raise error.order_operation_denied

            # udpate order
            orderprestatus = order.status
            order.status = 'canceling'
            detail = status.order_detail(**order)
            order.slog = status.append(form.operator, 'cancel', orderprestatus, order.status, detail, order.slog)

            order.save(d)

            del order['slog']
            self.write(protocol.success(data=order))


class CanceledHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            notify order canceled
        :return:
        """
        # get form arguments
        form = forms.order.Canceled(**self.cleaned_arguments)

        with models.db.atomic() as d, locker.order(form.id):
            # get order
            order = models.AccountOrder.filter(d, id=form.id).one()
            if order is None:
                raise error.order_not_exist
            if order.status not in ['canceling']:
                raise error.order_operation_denied

            # udpate order
            orderprestatus = order.status
            order.status = 'tcanceled'
            detail = status.order_detail(**order)
            order.slog = status.append(form.operator, 'cancel', orderprestatus, order.status, detail, order.slog)

            order.save(d)

            del order['slog']
            self.write(protocol.success(data=order))


class ExpiredHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            notify order canceled
        :return:
        """
        # get form arguments
        form = forms.order.Expired(**self.cleaned_arguments)

        with models.db.atomic() as d, locker.order(form.id):
            # get order
            order = models.AccountOrder.filter(d, id=form.id).one()
            if order is None:
                raise error.order_not_exist
            if order.status not in ['sent']:
                raise error.order_operation_denied

            # udpate order
            orderprestatus = order.status
            order.status = 'expired'
            detail = status.order_detail(**order)
            order.slog = status.append(form.operator, 'expire', orderprestatus, order.status, detail, order.slog)

            order.save(d)

            del order['slog']
            self.write(protocol.success(data=order))
