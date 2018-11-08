"""
    trade management
"""
import decimal, datetime, time
from tlib import rand
from .. import access, handler, forms, protocol, info, models, trade, locker, error, template, status


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
        trade.valid(form.stock, 'buy', form.optype, form.oprice, form.ocount)

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
            detail = '%s,%s,%s,%s,%s,%s' % ('buy', form.optype, form.oprice, form.ocount, '0.0', '0')
            slog = status.append(form.operator, form.otype, '', 'tobuy', detail) # status log
            usertrade = models.UserTrade(user_id=form.user, stock_id=form.stock, coupon_id=form.coupon_id,
                                        tcode=rand.uuid(), optype=form.optype, oprice=form.oprice, ocount=form.ocount, margin=margin,
                                        status='tobuy', slog=slog,
                                        ctime=int(time.time()), mtime=int(time.time()))

            # add trade order
            detail = '%s,%s,%s,%s,%s,%s' % (form.otype, form.optype, form.oprice, form.ocount, '0.0', '0')
            slog = status.append(form.operator, form.otype, '', 'notsend', detail)
            tradeorder = models.TradeOrder(tcode=form.tcode, account=form.account, scode=form.scode, sname=form.sname,
                                      otype=form.otype, optype=form.optype, oprice=form.oprice, ocount=form.ocount,
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
        trade.valid_trading_time('sell', form.optype)

        with models.db.atomic() as d, locker.user(form.user):
            # get user trade object
            usertrade = models.UserTrade.filter(d, id=form.trade, user_id=form.user, status='hold').one()
            if usertrade is None:
                raise error.trade_operation_denied

            # get stock object
            stock = models.Stock.filter(usertrade.stock_id).one()
            if stock is None or stock.status != 'normal':
                raise error.stock_is_closed

            # get or check current price
            if form.optype == 'sj':
                form.oprice = trade.get_trading_price(stock.id)
            else:
                trade.valid_trading_price(stock.id, form.oprice)

            #


class UserCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        pass


class SysBuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        pass


class SysSellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        pass


class SysCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        pass


class NotifyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        pass
