"""
    trade management
"""
import datetime, time, decimal, logging
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


class UpdateHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.Update(**self.cleaned_arguments)

        with models.db.atomic() as d:
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.id).one()
            if usertrade is None:
                raise error.trade_not_exist

            # lock user
            with locker.user(usertrade.user_id):
                # update
                usertrade.update(**form).save(d)

                # response data
                self.write(protocol.success(data=usertrade))


class UserBuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # check
        # get form arguments
        form = forms.trade.UserBuy(**self.cleaned_arguments)

        # get current
        if form.optype == 'sj':
            form.oprice = decimal.Decimal(trade.get_trading_price(form.stock)).quantize(decimal.Decimal('0.00'))

        # check trade time/count/price
        trade.valid(form.stock, form.optype, form.oprice, form.ocount)

        # today
        today = datetime.date.today()

        with models.db.atomic() as d, locker.user(form.user):
            # get user
            user = models.User.filter(d, id=form.user).one()
            if user is None or user.disable:
                raise error.user_has_disabled

            # get stock
            stock = models.Stock.filter(d, id=form.stock).one()
            if stock is None or stock.status!='open' or stock.limit in ['nobuy', 'nodelay']:
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
            margin = (capital / lever.lever).quantize(decimal.Decimal('0.00'))
            if user.money < margin:
                raise error.user_money_not_enough

            # use coupon
            if coupon is not None:
                coupon.status = 'used'
                coupon.utime = int(time.time())
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
            slog = status.append('user', 'buy', '', 'tobuy', detail) # status log
            usertrade = models.UserTrade(user_id=form.user, stock_id=form.stock, coupon_id=form.coupon,
                                        tcode=rand.uuid(), optype=form.optype, oprice=form.oprice, ocount=form.ocount, margin=margin,
                                        status='tobuy', slog=slog,
                                        ctime=int(time.time()), mtime=int(time.time())).save(d)

            # add trade order
            detail = '%s,%s,%s,%s,%s,%s' % ('buy', form.optype, form.oprice, form.ocount, '0.0', '0')
            slog = status.append('sys', 'buy', '', 'notsend', detail)
            tradeorder = models.TradeOrder(trade_id=usertrade.id, ocode=rand.uuid(), scode=stock.id, sname=stock.name,
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
                                             money=margin, ctime=int(time.time())).save(d)

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
            raise error.trade_operation_denied

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user, status='hold').one()
            if usertrade is None:
                raise error.trade_operation_denied

            # get stock object
            stock = models.Stock.filter(usertrade.stock_id).one()
            if stock is None or stock.status != 'open':
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
            usertrade.slog = status.append('user', 'sell', currentstatus, nextstatus, detail, usertrade.slog)
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
            orderstatus = {'notsend':'tcanceled', 'tosend':'tcanceled', 'sending':'tocancel', 'sent':'tocancel'}
            tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype=ordertype[usertrade.status], odate=today).one()
            if tradeorder is None or tradeorder.status not in orderstatus.keys():
                raise error.trade_operation_denied


            # update trade order status
            orderprestatsu = tradeorder.status
            tradeorder.status = orderstatus[orderprestatsu]
            tradeorder.slog = status.append('user', 'cancel', orderprestatsu, tradeorder.status, '', tradeorder.slog)
            tradeorder.save()

            # get next status
            tradeprestatus = usertrade.status
            usertrade.status = tradestatus[tradeprestatus]
            usertrade.slog = status.append('user', 'cancel', tradeprestatus, usertrade.status, '', usertrade.slog)

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

        with models.db.atomic() as d:
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, status='tobuy').one()
            if usertrade is None:
                raise error.trade_operation_denied

            with locker.user(usertrade.user_id):
                # get trade order object
                tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype='buy', status='notsend').one()
                if tradeorder is None:
                    raise error.trade_operation_denied

                # get&check stock status
                stock = models.Stock.filter(d, id=usertrade.stock_id).one()
                if stock is None or stock.status!='open' or stock.limit!='none':
                    raise error.stock_buy_limited

                # select a trade account
                tradeaccount = models.TradeAccount.filter(d, disable=False).orderby('money').desc().one()
                if tradeaccount is None:
                    raise error.account_not_usable

                # update trade order
                tradeorder.slog = status.append('sys', 'buy', 'notsend', 'tosend', '', tradeorder.slog)
                tradeorder.status = 'tosend'
                tradeorder.account = tradeaccount.account
                tradeorder.save(d)

                # update user trade
                usertrade.slog = status.append('sys', 'buy', usertrade.status, 'buying', '', usertrade.slog)
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

        with models.db.atomic() as d:
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, status__in=('tosell', 'toclose')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            with locker.user(usertrade.user_id):
                # get trade order object
                tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype='sell', status='notsend').one()
                if tradeorder is None:
                    raise error.trade_operation_denied

                # get&check stock status
                stock = models.Stock.filter(d, id=usertrade.stock_id)
                if stock is None or stock.status!='normal':
                    raise error.stock_is_closed

                # update trade order
                tradeorder.slog = status.append('sys', 'sell', 'notsend', 'tosend', '', tradeorder.slog)
                tradeorder.status = 'tosend'
                tradeorder.save(d)

                # update user trade
                tradeprestatus = usertrade.status
                tradestatus = {'tosell':'selling', 'toclose':'closing'}
                usertrade.status = tradestatus[tradeprestatus]
                usertrade.slog = status.append('sys', 'sell', tradeprestatus, usertrade.status, '', usertrade.slog)
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

        with models.db.atomic() as d:
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, status__in=('cancelbuy','cancelsell','cancelclose')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            with locker.user(usertrade.user_id):
                # get trade order object
                tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, status='tocancel').one()
                if tradeorder is None:
                    raise error.trade_operation_denied

                # update trade order
                tradeorder.slog = status.append('sys', 'cancel', 'tocancel', 'canceling', '', tradeorder.slog)
                tradeorder.status = 'canceling'
                tradeorder.save(d)

                # update user trade
                tradeprestatus = usertrade.status
                tradestatus = {'cancelbuy':'buycanceling', 'cancelsell':'sellcanceling', 'cancelclose':'closecanceling'}
                usertrade.status = tradestatus[tradeprestatus]
                usertrade.slog = status.append('sys', 'cancel', tradeprestatus, usertrade.status, '', usertrade.slog)
                usertrade.save(d)

                # response data
                data = {
                    'trade': usertrade,
                    'order': tradeorder
                }

                self.write(protocol.success(data=data))


class SysDropHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.SysDrop(**self.cleaned_arguments)

        # get today
        today = datetime.date.today()

        with models.db.atomic() as d:
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, status='tobuy').one()
            if usertrade is None:
                raise error.trade_operation_denied

            # lock user
            with locker.user(usertrade.user_id):
                # get trade order object
                tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype='buy', status='notsend').one()
                if tradeorder is None:
                    raise error.trade_operation_denied

                # update trade order status
                orderprestatsu = tradeorder.status
                tradeorder.status = 'tcanceled'
                tradeorder.slog = status.append('sys', 'drop', orderprestatsu, tradeorder.status, '', tradeorder.slog)
                tradeorder.save(d)

                # update trade record
                tradeprestatus = usertrade.status
                usertrade.status = 'canceled'
                usertrade.slog = status.append('sys', 'drop', tradeprestatus, usertrade.status, '', usertrade.slog)
                usertrade.save(d)

                # get user object
                user = models.User.filter(d, id=usertrade.user_id).one()

                # return coupon #
                if usertrade.coupon_id is not None:
                    usercoupon = models.UserCoupon.filter(d, id=usertrade.coupon_id).one()
                    usercoupon.status = 'notused'
                    usercoupon.utime = None
                    usercoupon.save(d)

                # return margin #
                # add bill
                models.UserBill(user_id=usertrade.user_id, code=rand.uuid(),
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


class OrderSentHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.OrderSent(**self.cleaned_arguments)

        with models.db.atomic() as d:
            # get trade order object
            tradeorder = models.TradeOrder.filter(d, id=form.id, status__in=('tosend', 'sending')).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id, status__in=('buying', 'selling','closing')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            # lock user
            with locker.user(usertrade.user_id):
                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.status = 'sent'
                tradeorder.slog = status.append('sys', 'send', orderprestatus, tradeorder.status, '', tradeorder.slog)
                tradeorder.mtime = int(time.time())
                tradeorder.save(d)

                # response data
                data = {
                    'trade': usertrade,
                    'order': tradeorder,
                }
                self.write(protocol.success(data=data))


class OrderBoughtHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.OrderBought(**self.cleaned_arguments)

        with models.db.atomic() as d:
            # get trade order object
            tradeorder = models.TradeOrder.filter(d, id=form.id, otype='buy', status__in=('sent', 'tocancel', 'canceling')).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id, status__in=('buying', 'cancelbuy','buycanceling')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            # lock user
            with locker.user(usertrade.user_id):
                # get trade lever
                tradelever = models.TradeLever.filter(d, trade_id=usertrade.id).one()
                if tradelever is None:
                    raise error.trade_operation_denied

                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.dprice = form.dprice
                tradeorder.dcount = form.dcount
                tradeorder.ddate = datetime.date.today()
                tradeorder.dtime = int(time.time())
                tradeorder.status = 'pdeal' if form.dcount < tradeorder.ocount else 'tdeal'
                tradeorder.slog = status.append('sys', 'bought', orderprestatus, tradeorder.status, '', tradeorder.slog)
                tradeorder.mtime = int(time.time())
                tradeorder.save(d)

                # compute open fee
                ofee = max(tradelever.ofmin, tradelever.ofrate*form.dprice*form.dcount)
                # add trade fee record
                tradefee = models.TradeFee(trade_id=usertrade.id, item=template.fee.open.item, detail=template.fee.open.detail % ofee,
                                           money=ofee, ctime=int(time.time())).save(d)

                # update user trade
                tradeprestatus = usertrade.status
                usertrade.ofee = ofee
                usertrade.hcount = tradeorder.dcount
                usertrade.hprice = tradeorder.dprice
                usertrade.fcount = 0
                usertrade.bcount = tradeorder.dcount
                usertrade.bprice = tradeorder.dprice
                usertrade.status = 'hold'
                usertrade.slog = status.append('sys', 'bought', tradeprestatus, usertrade.status, '', usertrade.slog)
                usertrade.mtime = int(time.time())
                usertrade.save(d)

                # response data
                data = {
                    'trade': usertrade,
                    'order': tradeorder,
                    'fee': tradefee
                }
                self.write(protocol.success(data=data))


class OrderSoldHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.OrderSold(**self.cleaned_arguments)

        with models.db.atomic() as d:
            # get trade order object
            tradeorder = models.TradeOrder.filter(d, id=form.id, otype='sell', status__in=('sent', 'tocancel', 'canceling')).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id, status__in=('selling', 'cancelsell','sellcanceling')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            # lock user
            with locker.user(usertrade.user_id):
                # get trade lever
                tradelever = models.TradeLever.filter(d, trade_id=usertrade.id).one()
                if tradelever is None:
                    raise error.trade_operation_denied

                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.dprice = form.dprice
                tradeorder.dcount = form.dcount
                tradeorder.ddate = datetime.date.today()
                tradeorder.dtime = int(time.time())
                tradeorder.status = 'pdeal' if form.dcount < tradeorder.ocount else 'tdeal'
                tradeorder.slog = status.append('sys', 'sold', orderprestatus, tradeorder.status, '', tradeorder.slog)
                tradeorder.mtime = int(time.time())
                tradeorder.save(d)

                # compute sold count&average price
                scount = tradeorder.dcount + usertrade.scount
                sprice = (tradeorder.dprice*tradeorder.dcount + usertrade.sprice*usertrade.scount) / scount

                # compute profit
                tprofit = scount * (sprice - usertrade.bprice)
                sprofit = max(decimal.Decimal('0.00'), tprofit*tradelever.psrate)

                # update user trade
                tradeprestatus = usertrade.status
                usertrade.hcount -= tradeorder.dcount
                usertrade.sprice = sprice
                usertrade.scount = scount
                usertrade.tprofit = tprofit
                usertrade.sprofit = sprofit
                usertrade.status = 'hold' if usertrade.hcount > 0 else 'sold'
                usertrade.slog = status.append('sys', 'sold', tradeprestatus, usertrade.status, '', usertrade.slog)
                usertrade.mtime = int(time.time())
                usertrade.save()

                # settlement
                if usertrade.status == 'sold':
                    # get user
                    user = models.User.filter(d, usertrade.user_id).one()
                    if user is None:
                        raise error.trade_operation_denied

                    # get coupon
                    coupon_cash, coupon_discount = decimal.Decimal('0.00'), decimal.Decimal('1.00')
                    if usertrade.coupon_id is not None:
                        usercoupon = models.UserCoupon.filter(d, id=usertrade.coupon_id).one()
                        if usercoupon.type == 'cash':
                            coupon_cash = usercoupon.value
                        if usercoupon.type == 'discount':
                            coupon_discount = usercoupon.value

                    # bill money
                    money = tprofit + usertrade.margin + coupon_cash - sprofit - (usertrade.ofee + usertrade.dfee)*coupon_discount
                    # bill detail
                    detail = template.bill.settle.detail % money
                    # add bill
                    models.UserBill(user_id=user.id, code=rand.uuid(),
                                    item=template.bill.settle.item, detail=detail,
                                    money=money, bmoney=user.money, lmoney=user.money+money, ctime=int(time.time())).save(d)

                    # update user
                    user.money += money
                    user.save(d)

                # response data
                data = {
                    'trade': usertrade,
                    'order': tradeorder
                }
                self.write(protocol.success(data=data))


class OrderCanceledHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.OrderCanceled(**self.cleaned_arguments)

        with models.db.atomic() as d:
            # get trade order object
            tradeorder = models.TradeOrder.filter(d, id=form.id, status__in=('canceling')).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id, status__in=('buycanceling', 'sellcanceling', 'closecanceling')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            # lock user
            with locker.user(usertrade.user_id):
                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.status = 'tcanceled'
                tradeorder.slog = status.append('sys', 'canceled', orderprestatus, tradeorder.status, '', tradeorder.slog)
                tradeorder.mtime = int(time.time())
                tradeorder.save(d)

                tradeprestatus = usertrade.status
                # update user trade
                if tradeprestatus in ('sellcanceling', 'closecanceling'):
                    # update free count
                    usertrade.fcount += tradeorder.ocount
                    usertrade.status = 'hold'
                else:
                    # return margin #
                    # get user object
                    user = models.User.filter(d, id=usertrade.user_id).one()

                    # add bill
                    models.UserBill(user_id=user.id, code=rand.uuid(),
                                    item=template.bill.settle.item, detail=template.bill.settle.detail%(usertrade.margin),
                                    money=usertrade.margin, bmoney=user.money, lmoney=user.money+usertrade.margin, ctime=int(time.time())).save(d)

                    # update user
                    user.money += usertrade.margin
                    user.save(d)

                    # update status
                    usertrade.status = 'canceled'
                usertrade.slog = status.append('sys', 'canceled', tradeprestatus, usertrade.status, '', usertrade.slog)
                usertrade.mtime = int(time.time())
                usertrade.save()

                # response data
                data = {
                    'trade': usertrade,
                    'order': tradeorder
                }
                self.write(protocol.success(data=data))


class OrderExpiredHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.OrderExpired(**self.cleaned_arguments)

        with models.db.atomic() as d:
            # get trade order object
            tradeorder = models.TradeOrder.filter(d, id=form.id, status__in=('sent')).one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id, status__in=('buying', 'selling', 'closing')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            # lock user
            with locker.user(usertrade.user_id):
                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.status = 'expired'
                tradeorder.slog = status.append('sys', 'expired', orderprestatus, tradeorder.status, '', tradeorder.slog)
                tradeorder.mtime = int(time.time())
                tradeorder.save(d)

                tradeprestatus = usertrade.status
                # update user trade
                if tradeprestatus in ('selling', 'closing'):
                    # update free count
                    usertrade.fcount += tradeorder.ocount
                    usertrade.status = 'hold'
                else:
                    # return margin #
                    # get user object
                    user = models.User.filter(d, id=usertrade.user_id).one()

                    # add bill
                    models.UserBill(user_id=user.id, code=rand.uuid(),
                                    item=template.bill.settle.item, detail=template.bill.settle.detail%(usertrade.margin),
                                    money=usertrade.margin, bmoney=user.money, lmoney=user.money+usertrade.margin, ctime=int(time.time())).save(d)

                    # update user
                    user.money += usertrade.margin
                    user.save(d)

                    # update status
                    usertrade.status = 'expired'
                usertrade.slog = status.append('sys', 'expired', tradeprestatus, usertrade.status, '', usertrade.slog)
                usertrade.mtime = int(time.time())
                usertrade.save()

                # response data
                data = {
                    'trade': usertrade,
                    'order': tradeorder
                }
                self.write(protocol.success(data=data))


class OrderUpdateHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.OrderUpdate(**self.cleaned_arguments)

        with models.db.atomic() as d:
            # get trade order object
            tradeorder = models.TradeOrder.filter(d, id=form.id).one()
            if tradeorder is None:
                raise error.order_not_exist

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id, status__in=('buying', 'selling', 'closing')).one()
            if usertrade is None:
                raise error.trade_not_exist

            # lock user
            with locker.user(usertrade.user_id):
                # update order
                tradeorder.update(**form).save(d)

                # response data
                self.write(protocol.success(data=tradeorder))
