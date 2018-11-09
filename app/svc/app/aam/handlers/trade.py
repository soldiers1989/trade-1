"""
    trade management
"""
import json, datetime, time, logging
from tlib import rand
from .. import access, handler, forms, protocol, models, trade, locker, error, template, status


class ListHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get trade records
        :return:
        """
        # list conditions
        conds = self.cleaned_arguments

        with models.db.create() as d:
            # get trade records
            trades = models.UserTrade.filter(d, **conds)

            # success
            self.write(protocol.success(data=trades))


class UserBuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # check
        # get form arguments
        form = forms.trade.UserBuy(**self.cleaned_arguments)

        # check trade time/count/price
        trade.valid(form.stock, form.optype, form.oprice, form.ocount)

        # check price when order is sj
        if form.optype == 'sj' and form.oprice < 1.02*trade.get_trading_price(form.stock):
            raise error.trade_less_margin

        # today
        today = datetime.date.today()

        with models.db.atomic() as d, locker.user(form.user):
            # get user
            user = models.User.filter(d, id=form.user).one()
            if user is None or user.disable:
                raise error.user_has_disabled

            # get stock
            stock = models.Stock.filter(d, id=form.stock).one()
            if stock is None or stock.status!='normal' or stock.limit in ['nobuy', 'nodelay']:
                raise error.stock_not_exist

            # get lever
            lever = models.Lever.filter(d, id=form.lever).one()
            if lever is None or lever.disable:
                raise error.lever_not_exist

            # get coupon
            coupon = None
            if form.coupon is not None:
                coupon = models.UserCoupon.filter(d, id=form.coupon).one()
                if coupon is None or coupon.user_id!=form.user or coupon.status!='notused' or not(coupon.sdate<=today<=coupon.edate):
                    raise error.coupon_not_exist

            # compute capital
            capital = form.oprice*form.ocount
            if not (lever.mmin<=capital<=lever.mmax):
                raise error.lever_capital_denied

            # compute margin
            margin = capital / lever.lever
            if user.money < margin:
                raise error.user_money_not_enough

            # use coupon
            if coupon is not None:
                coupon.status = 'used'
                coupon.save(d)

            # use money
            bmoney = user.money
            user.money -= margin
            user.save(d)

            # add bill
            userbill = models.UserBill(user_id=user.id, code=rand.uuid(),
                            item=template.bill.tmargin.item, detail=template.bill.tmargin.detail % str(margin),
                            money=margin, bmoney=bmoney, lmoney=user.money,
                            ctime=int(time.time())).save(d)

            # add user trade
            detail = '%s,%s,%s,%s,%s,%s,%s' % ('buy', form.optype, form.oprice, form.ocount, '0.0', '0', '0')
            slog = status.append('user', form.otype, '', 'tobuy', detail) # status log
            usertrade = models.UserTrade(user_id=form.user, stock_id=form.stock, coupon_id=form.coupon_id,
                                        tcode=rand.uuid(), optype=form.optype, oprice=form.oprice, ocount=form.ocount, margin=margin,
                                        status='tobuy', slog=slog,
                                        ctime=int(time.time()), mtime=int(time.time()))

            # add trade order
            detail = '%s,%s,%s,%s,%s,%s' % ('buy', form.optype, form.oprice, form.ocount, '0.0', '0')
            slog = status.append('sys', 'buy', '', 'notsend', detail)
            tradeorder = models.TradeOrder(trade_id=usertrade.id, tcode=usertrade.tcode, scode=stock.id, sname=stock.name,
                                           otype='buy', optype=form.optype, oprice=form.oprice, ocount=form.ocount,
                                           odate=datetime.date.today(), otime=int(time.time()),
                                           dprice=0.0, dcount=0, status='notsend', slog=slog,
                                           ctime=int(time.time()), mtime=int(time.time())).save(d)


            # add lever record
            tradelever = models.TradeLever(trade_id=usertrade.id, lever=lever.lever, wline=lever.wline, sline=lever.sline,
                                           ofmin=lever.ofmin, ofrate=lever.ofrate, dfrate=lever.dfrate, psrate=lever.psrate,
                                           mmin=lever.mmin, mmax=lever.mmax).save(d)

            # add trade margin record
            trademargin = models.TradeMargin(trade_id=usertrade.id, item=template.margin.init.item, detail=template.margin.init.detail%str(margin),
                                             money=margin, ctime=int(time.time()))

            # response data
            data = {
                'trade': usertrade,
                'order': tradeorder,
                'lever': tradelever,
                'margin': trademargin,
                'bill': userbill,
                'user': user
            }

            self.write(protocol.success(data=data))


class UserSellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.UserSell(**self.cleaned_arguments)

        # check trading time
        trade.valid_trading_time(form.optype)

        # check sell type
        if form.type not in ['sell', 'close']:
            raise error.invalid_parameters

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user, status='hold').one()
            if usertrade is None:
                raise error.trade_operation_denied

            # get stock object
            stock = models.Stock.filter(usertrade.stock_id).one()
            if stock is None or stock.status != 'normal':
                raise error.stock_is_closed

            # get & check sell price
            if form.optype == 'sj':
                form.oprice = trade.get_trading_price(stock.id)
            else:
                trade.valid_trading_price(stock.id, form.oprice)

            # get & check sell count
            if form.ocount > usertrade.fcount:
                raise error.stock_count_not_enough

            # add trade order
            detail = '%s,%s,%s,%s,%s,%s' % ('sell', form.optype, form.oprice, form.ocount, '0.0', '0')
            slog = status.append('user', 'sell', '', 'notsend', detail)
            tradeorder = models.TradeOrder(trade_id=usertrade.id, tcode=usertrade.tcode, account=usertrade.account, scode=stock.id, sname=stock.name,
                                           otype='sell', optype=form.optype, oprice=form.oprice, ocount=form.ocount,
                                           odate=datetime.date.today(), otime=int(time.time()),
                                           dprice=0.0, dcount=0, status='notsend', slog=slog,
                                           ctime=int(time.time()), mtime=int(time.time())).save(d)

            # update user trade
            currentstatus, nextstatus = usertrade.status, 'tosell' if form.type=='sell' else 'toclose'
            detail = '%s,%s,%s,%s,%s,%s,%s' % ('sell', form.optype, form.oprice, form.ocount, usertrade.hprice, usertrade.hcount, usertrade.fcount)
            usertrade.slog = status.append('user', 'sell', currentstatus, nextstatus, detail)
            usertrade.status = nextstatus
            usertrade.fcount -= form.ocount
            usertrade.save(d)

            # response data
            data = {
                'trade': usertrade,
                'order': tradeorder
            }

            self.write(protocol.success(data=data))


class UserCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.UserCancel(**self.cleaned_arguments)

        # get today
        today = datetime.date.today()

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            tradestatus = {'tobuy': 'canceled', 'tosell': 'hold', 'toclose': 'hold', 'buying': 'cancelbuy', 'selling': 'cancelsell', 'closing': 'cancelclose'}
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user).one()
            if usertrade is None or usertrade.status not in tradestatus.keys():
                raise error.trade_operation_denied

            # get trade order object
            ordertype = {'tobuy': 'buy', 'tosell': 'sell', 'toclose': 'sell', 'buying': 'buy', 'selling': 'sell', 'closing': 'sell'}
            orderstatus = {'notsend':'tcanceled', 'tosend':'tocancel', 'sending':'tocancel', 'sent':'tocancel'}
            tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype=ordertype[usertrade.status], odate=today).one()
            if tradeorder is None or tradeorder.status not in orderstatus.keys():
                raise error.trade_operation_denied


            # update trade order status
            orderprestatsu = tradeorder.status
            tradeorder.status = orderstatus[orderprestatsu]
            tradeorder.slog = status.append('user', 'cancel', orderprestatsu, tradeorder.status, '')
            tradeorder.save()

            # get next status
            tradeprestatus = usertrade.status
            usertrade.status = tradestatus[tradeprestatus]
            usertrade.slog = status.append('user', 'cancel', tradeprestatus, usertrade.status, '')

            # process cancel operation
            if usertrade.status == 'canceled': # -> canceled
                # get user object
                user = models.User.filter(d, id=usertrade.user_id).one()

                # return margin #
                # add bill
                models.UserBill(user_id=usertrade.id, code=rand.uuid(),
                               item=template.bill.rmargin.item, detail=template.bill.rmargin.detail % str(usertrade.margin),
                               money=usertrade.margin, bmoney=user.money, lmoney=user.money+usertrade.margin,
                               ctime=int(time.time())).save(d)

                # add money
                user.money += usertrade.margin
                user.save(d)
            elif usertrade.status == 'hold': # ->hold
                usertrade.fcount = usertrade.hcount
            else:
                pass

            # update trade record
            usertrade.save(d)

            # response data
            data = {
                'trade': usertrade,
                'order': tradeorder
            }
            self.write(protocol.success(data=data))


class SysBuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.SysBuy(**self.cleaned_arguments)

        # get today
        today = datetime.date.today()

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user, status='tobuy').one()
            if usertrade is None:
                raise error.trade_operation_denied

            # get trade order object
            tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype='buy', status='notsend', odate=today).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # get&check stock status
            stock = models.Stock.filter(d, id=usertrade.stock_id)
            if stock is None or stock.status!='normal' or stock.limit!='none':
                raise error.stock_buy_limited

            # select a trade account
            tradeaccount = models.TradeAccount.filter(d, disable=False).orderby('money').desc().one()
            if tradeaccount is None:
                raise error.account_not_usable

            # update trade order
            tradeorder.slog = status.append('sys', 'buy', 'notsend', 'tosend', '')
            tradeorder.status = 'tosend'
            tradeorder.account = tradeaccount.account
            tradeorder.save(d)

            # update user trade
            usertrade.slog = status.append('sys', 'buy', usertrade.status, 'buying', '')
            usertrade.status = 'buying'
            usertrade.save(d)

            # response data
            data = {
                'trade': usertrade,
                'order': tradeorder
            }

            self.write(protocol.success(data=data))


class SysSellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.SysSell(**self.cleaned_arguments)

        # get today
        today = datetime.date.today()

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user, status__in=('tosell', 'toclose')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            # get trade order object
            tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype='sell', status='notsend', odate=today).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # get&check stock status
            stock = models.Stock.filter(d, id=usertrade.stock_id)
            if stock is None or stock.status!='normal':
                raise error.stock_is_closed

            # update trade order
            tradeorder.slog = status.append('sys', 'sell', 'notsend', 'tosend', '')
            tradeorder.status = 'tosend'
            tradeorder.save(d)

            # update user trade
            tradeprestatus = usertrade.status
            tradestatus = {'tosell':'selling', 'toclose':'closing'}
            usertrade.status = tradestatus[tradeprestatus]
            usertrade.slog = status.append('sys', 'sell', tradeprestatus, usertrade.status, '')
            usertrade.save(d)

            # response data
            data = {
                'trade': usertrade,
                'order': tradeorder
            }

            self.write(protocol.success(data=data))


class SysCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.SysCancel(**self.cleaned_arguments)

        # get today
        today = datetime.date.today()

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user, status__in=('cancelbuy','cancelsell','cancelclose')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            # get trade order object
            tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, status='tocancel', odate=today).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # update trade order
            tradeorder.slog = status.append('sys', 'cancel', 'tocancel', 'canceling', '')
            tradeorder.status = 'canceling'
            tradeorder.save(d)

            # update user trade
            tradeprestatus = usertrade.status
            tradestatus = {'cancelbuy':'buycanceling', 'cancelsell':'sellcanceling', 'cancelclose':'closecanceling'}
            usertrade.status = tradestatus[tradeprestatus]
            usertrade.slog = status.append('sys', 'cancel', tradeprestatus, usertrade.status, '')
            usertrade.save(d)

            # response data
            data = {
                'trade': usertrade,
                'order': tradeorder
            }

            self.write(protocol.success(data=data))


class SysBoughtHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.SysBought(**self.cleaned_arguments)


class SysSoldHandler(handler.Handler):
    pass


class SysCanceledHandler(handler.Handler):
    pass


class SysDroppedHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.SysDropped(**self.cleaned_arguments)

        # get today
        today = datetime.date.today()

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user, status='tobuy').one()
            if usertrade is None:
                raise error.trade_operation_denied

            # get trade order object
            tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype='notsend', odate=today).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # update trade order status
            orderprestatsu = tradeorder.status
            tradeorder.status = 'tcanceled'
            tradeorder.slog = status.append('sys', 'drop', orderprestatsu, tradeorder.status, '')
            tradeorder.save()

            # update trade record
            tradeprestatus = usertrade.status
            usertrade.status = 'canceled'
            usertrade.slog = status.append('sys', 'drop', tradeprestatus, usertrade.status, '')
            usertrade.save(d)

            # get user object
            user = models.User.filter(d, id=usertrade.user_id).one()

            # return margin #
            # add bill
            models.UserBill(user_id=usertrade.id, code=rand.uuid(),
                            item=template.bill.rmargin.item, detail=template.bill.rmargin.detail % str(usertrade.margin),
                            money=usertrade.margin, bmoney=user.money, lmoney=user.money + usertrade.margin,
                            ctime=int(time.time())).save(d)

            # add money
            user.money += usertrade.margin
            user.save(d)

            # response data
            data = {
                'trade': usertrade,
                'order': tradeorder
            }
            self.write(protocol.success(data=data))


class SysSyncHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order notify, post data format:
            [
                {account:account, ocode:ocode, dprice:dprice, dcount:dcount, status:status, operator:operator},
                ......
            ]

            status to process:

        :return:
        """
        # get notify orders
        notifyorders = json.loads(self.request.body.decode())

        # validate notify orders
        for notifyorder in notifyorders:
            if not {'account','ocode','dprice','dcount','status','operator'}.issubset(set(notifyorder.keys())):
                raise error.order_notify_data
            if notifyorder['status'] not in ['sent','canceling','pcanceled','tcanceled','fcanceled','pdeal','tdeal','dropped']:
                raise error.order_notify_data

        with models.db.atomic() as d:
            # get all pending orders of today
            localorders = models.TradeOrder.filter(d, odate=datetime.date.today(), ocode__null=True, status__in=('notsend, tosend, sending, sent, tocancel, canceling, pdeal')).all()

            # updated orders
            updatedorders = []

            # process each order
            for notifyorder in notifyorders:
                for localorder in localorders:

                    if notifyorder['account']==localorder.account and notifyorder['ocode']==localorder.ocode and notifyorder['status']:
                        pass



            # response data
            data = {
                'updated': len(updatedorders),
                'updates': updatedorders
            }
            self.write(protocol.success(data=data))
