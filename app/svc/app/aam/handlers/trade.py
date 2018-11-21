"""
    trade management
"""
import datetime, time, decimal
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
            trades = models.UserTrade.filter(d, **conds).all()

            # remote slog field
            for trade in trades:
                del trade['slog']

            # success
            self.write(protocol.success(data=trades))


class ClearHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            clear user trade daily fees
        :return:
        """
        with models.db.create() as d:
            # get user trade which has holding count
            usertrades = models.UserTrade.filter(d, hcount__gt=0).all()

            # get today
            today = datetime.date.today()

            cleared, failed = [], []
            # clear user trade
            for usertrade in usertrades:
                try:
                    # get delay days
                    cday = datetime.date.fromtimestamp(usertrade.ctime)
                    days, cleareddays, clearedfees = (today-cday).days+1, usertrade.dday, usertrade.dfee

                    # already cleared
                    if days <= cleareddays:
                        continue

                    # get user trade lever
                    tradelever = models.TradeLever.filter(d, trade_id=usertrade.id).one()

                    # capital used
                    capital = usertrade.hcount*usertrade.hprice
                    # compute delay fees
                    deltadays = days - cleareddays
                    deltfees = deltadays*capital*tradelever.dfrate

                    # add trade fee record
                    models.TradeFee(trade_id=usertrade.id, item=template.fee.delay.item, detail=template.fee.delay.detail % deltfees,
                                               money=deltfees, ctime=int(time.time())).save(d)

                    # update user trade
                    usertrade.dday += deltadays
                    usertrade.dfee += deltfees
                    usertrade.save(d)

                    # commit
                    d.commit()

                    # remote slog
                    del usertrade['slog']
                    cleared.append(usertrade)
                except Exception as e:
                    del usertrade['slog']
                    failed.append(usertrade)
                    d.rollback()

            # response data
            data = {
                'cleared': cleared,
                'failed': failed
            }
            # success
            self.write(protocol.success(data=data))


class UpdateHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.Update(**self.cleaned_arguments)

        # get update items
        updateitems = {}
        for k in self.cleaned_arguments:
            updateitems[k] = form[k]

        with models.db.atomic() as d:
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.id).one()
            if usertrade is None:
                raise error.trade_not_exist

            # lock user
            with locker.user(usertrade.user_id):
                # update trade
                tradeprestatus = usertrade.status
                usertrade.update(**updateitems)
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'update', tradeprestatus, usertrade.status, detail, usertrade.slog)
                usertrade.save(d)

                # response data
                del usertrade['slog']
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
            form.oprice = trade.get_trading_price(form.stock)

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
            margin = capital / lever.lever
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
            usertrade = models.UserTrade(user_id=form.user, stock_id=form.stock, coupon_id=form.coupon,
                                        tcode=rand.uuid(), optype=form.optype, oprice=form.oprice, ocount=form.ocount, margin=margin, amargin=0,
                                        status='tobuy', ctime=int(time.time()), mtime=int(time.time()))
            detail = status.trade_detail(**usertrade)
            usertrade.slog = status.append('user', 'buy', '', 'tobuy', detail)
            usertrade.save(d)

            # add trade order
            tradeorder = models.TradeOrder(trade_id=usertrade.id, ocode=rand.uuid(), scode=stock.id, sname=stock.name,
                                           otype='buy', optype=form.optype, oprice=form.oprice, ocount=form.ocount,
                                           odate=datetime.date.today(), otime=int(time.time()),
                                           dprice=0.0, dcount=0, status='notsend', ctime=int(time.time()), mtime=int(time.time()))
            detail = status.order_detail(**tradeorder)
            tradeorder.slog = status.append('sys', 'buy', '', 'notsend', detail)
            tradeorder.save(d)


            # add lever record
            tradelever = models.TradeLever(trade_id=usertrade.id, lever=lever.lever, wline=lever.wline, sline=lever.sline,
                                           ofmin=lever.ofmin, ofrate=lever.ofrate, dfrate=lever.dfrate, psrate=lever.psrate,
                                           mmin=lever.mmin, mmax=lever.mmax).save(d)

            # add trade margin record
            trademargin = models.TradeMargin(trade_id=usertrade.id, item=template.margin.init.item, detail=template.margin.init.detail%str(margin),
                                             prepay=margin, money=margin, ctime=int(time.time())).save(d)

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
            stock = models.Stock.filter(d, id=usertrade.stock_id).one()
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
            tradeorder = models.TradeOrder(trade_id=usertrade.id, ocode=rand.uuid(), account=usertrade.account, scode=stock.id, sname=stock.name,
                                           otype='sell', optype=form.optype, oprice=form.oprice, ocount=form.ocount,
                                           odate=datetime.date.today(), otime=int(time.time()),
                                           dprice=0.0, dcount=0, status='notsend',
                                           ctime=int(time.time()), mtime=int(time.time()))
            detail = status.order_detail(**tradeorder)
            tradeorder.slog = status.append('user', 'sell', '', 'notsend', detail)
            tradeorder.save(d)

            # update user trade
            currentstatus, nextstatus = usertrade.status, 'tosell' if form.type=='sell' else 'toclose'
            usertrade.status = nextstatus
            usertrade.fcount -= form.ocount
            detail = status.trade_detail(**usertrade)
            usertrade.slog = status.append('user', 'sell', currentstatus, usertrade.status, detail, usertrade.slog)
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

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            tradestatus = {'tobuy': 'canceled', 'tosell': 'hold', 'toclose': 'hold', 'buying': 'cancelbuy', 'selling': 'cancelsell', 'closing': 'cancelclose'}
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user).one()
            if usertrade is None or usertrade.status not in tradestatus.keys():
                raise error.trade_operation_denied

            # get trade order object
            ordertype = {'tobuy': 'buy', 'tosell': 'sell', 'toclose': 'sell', 'buying': 'buy', 'selling': 'sell', 'closing': 'sell'}
            orderstatus = {'notsend':'tcanceled', 'tosend':'tcanceled', 'sending':'sending', 'sent':'sent'}
            tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, otype=ordertype[usertrade.status], status__in=list(orderstatus.keys())).one()
            if tradeorder is None or tradeorder.status not in orderstatus.keys():
                raise error.trade_operation_denied


            # update trade order status
            orderprestatsu = tradeorder.status
            tradeorder.status = orderstatus[orderprestatsu]
            detail = status.order_detail(**tradeorder)
            tradeorder.slog = status.append('user', 'cancel', orderprestatsu, tradeorder.status, detail, tradeorder.slog)
            tradeorder.save(d)

            # get next status
            tradeprestatus = usertrade.status

            # next trade status
            usertrade.status = tradestatus[tradeprestatus]
            # process when order has canceled
            if tradeorder.status == 'tcanceled':
                if tradeprestatus in ['tosell', 'toclose', 'selling', 'closing']:
                    usertrade.status = 'hold'
                elif tradeprestatus in ['tobuy', 'buying']:
                    usertrade.status = 'canceled'
                else:
                    pass

            # process cancel operation
            if usertrade.status == 'canceled': # -> canceled
                # get user object
                user = models.User.filter(d, id=usertrade.user_id).one()

                # return coupon #
                if usertrade.coupon_id is not None:
                    usercoupon = models.UserCoupon.filter(d, id=usertrade.coupon_id).one()
                    usercoupon.status = 'notused'
                    usercoupon.utime = None
                    usercoupon.save(d)

                # return init margin #
                # add bill
                models.UserBill(user_id=usertrade.id, code=rand.uuid(),
                               item=template.bill.rmargin.item, detail=template.bill.rmargin.detail % str(usertrade.margin),
                               money=usertrade.margin, bmoney=user.money, lmoney=user.money+usertrade.margin,
                               ctime=int(time.time())).save(d)

                # add money
                user.money += usertrade.margin
                user.save(d)
            elif usertrade.status == 'hold': # ->hold
                usertrade.fcount += tradeorder.ocount
            else:
                pass

            # update trade record
            detail = status.trade_detail(**usertrade)
            usertrade.slog = status.append('user', 'cancel', tradeprestatus, usertrade.status, detail, usertrade.slog)
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
                orderprestatus = tradeorder.status
                tradeorder.status = 'tosend'
                tradeorder.account = tradeaccount.account
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'buy', orderprestatus, tradeorder.status, detail, tradeorder.slog)
                tradeorder.save(d)

                # update user trade
                tradeprestatus = usertrade.status
                usertrade.account = tradeaccount.account
                usertrade.status = 'buying'
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'buy', tradeprestatus, usertrade.status, detail, usertrade.slog)
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
                stock = models.Stock.filter(d, id=usertrade.stock_id).one()
                if stock is None or stock.status!='open':
                    raise error.stock_is_closed

                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.status = 'tosend'
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'sell', orderprestatus, tradeorder.status, detail, tradeorder.slog)
                tradeorder.save(d)

                # update user trade
                tradeprestatus = usertrade.status
                tradestatus = {'tosell':'selling', 'toclose':'closing'}
                usertrade.status = tradestatus[tradeprestatus]
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'sell', tradeprestatus, usertrade.status, detail, usertrade.slog)
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

        with models.db.atomic() as d:
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, status__in=('cancelbuy','cancelsell','cancelclose')).one()
            if usertrade is None:
                raise error.trade_operation_denied

            with locker.user(usertrade.user_id):
                # get trade order object
                tradeorder = models.TradeOrder.filter(d, trade_id=usertrade.id, status__in=('sending','sent')).one()
                if tradeorder is None:
                    raise error.trade_operation_denied

                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.status = 'tocancel'
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'cancel', orderprestatus, tradeorder.status, detail, tradeorder.slog)
                tradeorder.save(d)

                # update user trade
                tradeprestatus = usertrade.status
                tradestatus = {'cancelbuy':'buycanceling', 'cancelsell':'sellcanceling', 'cancelclose':'closecanceling'}
                usertrade.status = tradestatus[tradeprestatus]
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'cancel', tradeprestatus, usertrade.status, detail, usertrade.slog)
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
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'drop', orderprestatsu, tradeorder.status, detail, tradeorder.slog)
                tradeorder.save(d)

                # update trade record
                tradeprestatus = usertrade.status
                usertrade.status = 'canceled'
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'drop', tradeprestatus, usertrade.status, detail, usertrade.slog)
                usertrade.save(d)

                # get user object
                user = models.User.filter(d, id=usertrade.user_id).one()

                # return coupon #
                if usertrade.coupon_id is not None:
                    usercoupon = models.UserCoupon.filter(d, id=usertrade.coupon_id).one()
                    usercoupon.status = 'notused'
                    usercoupon.utime = None
                    usercoupon.save(d)

                # return init margin #
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


class OrderListHandler(handler.Handler):
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
            # get trade orders
            orders = models.TradeOrder.filter(d, **conds).all()

            # remote slog field
            for order in orders:
                del order['slog']

            # success
            self.write(protocol.success(data=orders))


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
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id).one()
            if usertrade is None or usertrade.status not in ('buying', 'selling','closing'):
                raise error.trade_operation_denied

            # lock user
            with locker.user(usertrade.user_id):
                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.status = 'sent'
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'send', orderprestatus, tradeorder.status, detail, tradeorder.slog)
                tradeorder.mtime = int(time.time())
                tradeorder.save(d)

                # response data
                data = {
                    'trade': usertrade,
                    'order': tradeorder,
                }
                self.write(protocol.success(data=data))


class OrderCancelingHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get form arguments
        form = forms.trade.OrderCanceling(**self.cleaned_arguments)

        with models.db.atomic() as d:
            # get trade order object
            tradeorder = models.TradeOrder.filter(d, id=form.id, status='tocancel').one()
            if tradeorder is None:
                raise error.trade_operation_denied

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id).one()
            if usertrade is None or usertrade.status not in ['buycanceling', 'sellcanceling', 'closecanceling']:
                raise error.trade_operation_denied

            # lock user
            with locker.user(usertrade.user_id):
                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.status = 'canceling'
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'send', orderprestatus, tradeorder.status, detail, tradeorder.slog)
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
                raise error.order_not_exist

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id, status__in=('buying', 'cancelbuy','buycanceling')).one()
            if usertrade is None:
                raise error.trade_not_exist

            # lock user
            with locker.user(usertrade.user_id):
                # get trade lever
                tradelever = models.TradeLever.filter(d, trade_id=usertrade.id).one()
                if tradelever is None:
                    raise error.trade_lever_not_exist

                # update trade order
                orderprestatus = tradeorder.status
                tradeorder.dprice = form.dprice
                tradeorder.dcount = form.dcount
                tradeorder.ddate = datetime.date.today()
                tradeorder.dtime = int(time.time())
                tradeorder.status = 'pdeal' if form.dcount < tradeorder.ocount else 'tdeal'
                tradeorder.mtime = int(time.time())
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'bought', orderprestatus, tradeorder.status, detail, tradeorder.slog)
                tradeorder.save(d)

                # compute open fee
                ofee = max(tradelever.ofmin, tradelever.ofrate*form.dprice*form.dcount)
                # add trade fee record
                tradefee = models.TradeFee(trade_id=usertrade.id, item=template.fee.open.item, detail=template.fee.open.detail % ofee,
                                           money=ofee, ctime=int(time.time())).save(d)

                # return extra margin
                margin = (tradeorder.dcount*tradeorder.dprice) / tradelever.lever
                if usertrade.margin > margin:
                    # upate trade margin
                    trademargin = models.TradeMargin.filter(d, trade_id=usertrade.id).one()
                    if trademargin is None:
                        raise error.trade_margin_not_exist
                    trademargin.money = margin
                    trademargin.save(d)

                    # extra margin
                    extramargin = usertrade.margin - margin
                    # get trade user
                    tradeuser = models.User.filter(d, id=usertrade.user_id).one()
                    if tradeuser is None:
                        raise error.trade_user_not_exist

                    # add user bill
                    userbill = models.UserBill(user_id=tradeuser.id, code=rand.uuid(),item=template.bill.rmargin.item, detail=template.bill.rmargin.detail%(extramargin),
                                               money=extramargin, bmoney=tradeuser.money, lmoney=tradeuser.money+extramargin, ctime=int(time.time()))
                    userbill.save(d)

                    # udpate user money
                    tradeuser.money = tradeuser.money + extramargin
                    tradeuser.save(d)

                    # update user trade
                    usertrade.margin = margin

                # update user trade
                tradeprestatus = usertrade.status
                usertrade.ofee = ofee
                usertrade.hcount = tradeorder.dcount
                usertrade.hprice = tradeorder.dprice
                usertrade.fcount = 0
                usertrade.bcount = tradeorder.dcount
                usertrade.bprice = tradeorder.dprice
                usertrade.status = 'hold'
                usertrade.mtime = int(time.time())
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'bought', tradeprestatus, usertrade.status, detail, usertrade.slog)
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
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id, status__in=('selling', 'cancelsell','sellcanceling', 'closing', 'cancelclose', 'closecanceling')).one()
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
                tradeorder.mtime = int(time.time())
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'sold', orderprestatus, tradeorder.status, detail, tradeorder.slog)
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
                usertrade.status = 'hold' if usertrade.hcount > 0 else 'sold' if tradeprestatus in ['selling','cancelsell','sellcanceling'] else 'closed'
                usertrade.mtime = int(time.time())
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'sold', tradeprestatus, usertrade.status, detail, usertrade.slog)
                usertrade.save(d)

                # settlement
                if usertrade.status in ['sold','closed']:
                    # get user
                    user = models.User.filter(d, id=usertrade.user_id).one()
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
                    money = tprofit + usertrade.margin  + usertrade.amargin + coupon_cash - sprofit - (usertrade.ofee + usertrade.dfee)*coupon_discount
                    clearmoney = decimal.Decimal('0.00') if money < 0 else money
                    # bill detail
                    detail = template.bill.settle.detail % money.quantize(decimal.Decimal('0.00'))
                    # add bill
                    models.UserBill(user_id=user.id, code=rand.uuid(),
                                    item=template.bill.settle.item, detail=detail,
                                    money=money, bmoney=user.money, lmoney=user.money+clearmoney, ctime=int(time.time())).save(d)

                    # update user
                    user.money += clearmoney
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
                tradeorder.mtime = int(time.time())
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'canceled', orderprestatus, tradeorder.status, detail, tradeorder.slog)
                tradeorder.save(d)

                tradeprestatus = usertrade.status
                # update user trade
                if tradeprestatus in ('sellcanceling', 'closecanceling'):
                    # update free count
                    usertrade.fcount += tradeorder.ocount
                    usertrade.status = 'hold'
                else:
                    # get user object
                    user = models.User.filter(d, id=usertrade.user_id).one()

                    # return coupon #
                    if usertrade.coupon_id is not None:
                        usercoupon = models.UserCoupon.filter(d, id=usertrade.coupon_id).one()
                        usercoupon.status = 'notused'
                        usercoupon.utime = None
                        usercoupon.save(d)

                    # return initial margin #
                    # add bill
                    models.UserBill(user_id=user.id, code=rand.uuid(),
                                    item=template.bill.rmargin.item, detail=template.bill.rmargin.detail%(usertrade.margin),
                                    money=usertrade.margin, bmoney=user.money, lmoney=user.money+usertrade.margin, ctime=int(time.time())).save(d)

                    # update user
                    user.money += usertrade.margin
                    user.save(d)

                    # update status
                    usertrade.status = 'canceled'

                usertrade.mtime = int(time.time())
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'canceled', tradeprestatus, usertrade.status, detail, usertrade.slog)
                usertrade.save(d)

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
                tradeorder.mtime = int(time.time())
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'expired', orderprestatus, tradeorder.status, detail, tradeorder.slog)
                tradeorder.save(d)

                tradeprestatus = usertrade.status
                # update user trade
                if tradeprestatus in ('selling', 'closing'):
                    # update free count
                    usertrade.fcount += tradeorder.ocount
                    usertrade.status = 'hold'
                else:
                    # get user object
                    user = models.User.filter(d, id=usertrade.user_id).one()

                    # return coupon #
                    if usertrade.coupon_id is not None:
                        usercoupon = models.UserCoupon.filter(d, id=usertrade.coupon_id).one()
                        usercoupon.status = 'notused'
                        usercoupon.utime = None
                        usercoupon.save(d)

                    # return initial margin #
                    # add bill
                    models.UserBill(user_id=user.id, code=rand.uuid(),
                                    item=template.bill.settle.item, detail=template.bill.settle.detail%(usertrade.margin),
                                    money=usertrade.margin, bmoney=user.money, lmoney=user.money+usertrade.margin, ctime=int(time.time())).save(d)

                    # update user
                    user.money += usertrade.margin
                    user.save(d)

                    # update status
                    usertrade.status = 'expired'
                usertrade.mtime = int(time.time())
                detail = status.trade_detail(**usertrade)
                usertrade.slog = status.append('sys', 'expired', tradeprestatus, usertrade.status, detail, usertrade.slog)
                usertrade.save(d)

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

        # get update items
        updateitems = {}
        for k in self.cleaned_arguments:
            updateitems[k] = form[k]

        with models.db.atomic() as d:
            # get trade order object
            tradeorder = models.TradeOrder.filter(d, id=form.id).one()
            if tradeorder is None:
                raise error.order_not_exist

            # get user trade object
            usertrade = models.UserTrade.filter(d, id=tradeorder.trade_id).one()
            if usertrade is None:
                raise error.trade_not_exist

            # lock user
            with locker.user(usertrade.user_id):
                # update order
                orderprestatus = tradeorder.status
                tradeorder.update(**updateitems)
                detail = status.order_detail(**tradeorder)
                tradeorder.slog = status.append('sys', 'update', orderprestatus, tradeorder.status, detail, tradeorder.slog)
                tradeorder.save(d)

                # response data
                self.write(protocol.success(data=tradeorder))
