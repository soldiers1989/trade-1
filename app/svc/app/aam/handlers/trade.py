"""
    trade management
"""
import datetime, time
from app import rules
from app.util import rand
from app.aam import suite, access, handler, daos, forms, protocol, error, info, lock


class UserBuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new trade request
        :return:
        """
        ## get arguments ##
        form = forms.trade.UserBuy(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_buy_time(form.ptype, time.time()):
            raise error.not_trading_time

        ## process trade add operation by lock user ##
        with lock.user(form.user):
            # init trade dao #
            tradeDao = daos.trade.TradeDao(self.db)
            userDao = daos.user.UserDao(self.db)
            stockDao = daos.stock.StockDao(self.db)
            leverDao = daos.lever.LeverDao(self.db)
            couponDao = daos.coupon.CouponDao(self.db)
            accountDao = daos.account.AccountDao(self.db)

            ## check arguments ##
            # check user
            user = userDao.get(id=form.user)
            if user is None:
                raise error.user_not_exist
            if user.disable:
                raise error.user_has_disabled

            # check stock
            stock = stockDao.get(id=form.stock)
            if stock is None:
                raise error.stock_not_exist
            if stock.status == suite.enum.stock.closed:
                raise error.stock_is_closed
            if stock.status == suite.enum.stock.delisted:
                raise error.stock_is_delisted
            if stock.limit == suite.enum.risk.nobuy or stock.limit == suite.enum.risk.nodelay:
                raise error.stock_buy_limited

            # check lever
            lever = leverDao.get(id=form.lever)
            if lever is None:
                raise error.lever_not_exist
            if lever.disable:
                raise error.lever_has_disabled

            # check stock count
            if not rules.trade.valid_buy_count(form.count):
                raise error.stock_count_error

            # check order price
            if form.price is None or not rules.trade.valid_buy_price(form.stock, form.price):
                raise error.stock_price_error

            # check capital
            capital = form.price * form.count
            account = accountDao.select_one()
            if account is None or account.lmoney < capital:
                raise error.account_money_not_enough

            # check lever money limit
            if capital > lever.mmax or capital< lever.mmin:
                raise error.lever_capital_denied

            # check coupon
            coupon_id, coupon_money = None, 0.0
            if form.coupon is not None:
                coupon = couponDao.get(id=form.coupon)
                if coupon is None:
                    raise error.coupon_not_exist
                if coupon.user_id != form.user:
                    raise error.invalid_parameters
                if coupon.status != suite.enum.coupon.unused.code:
                    raise error.coupon_has_used

                today = datetime.date.today()
                if today < coupon.sdate or today > coupon.edate:
                    raise error.coupon_has_expired

                coupon_id = coupon.id
                coupon_money = coupon.money

            # compute margin
            margin = capital / lever.lever

            # compute order money
            cost = margin - coupon_money

            # check user left money
            before_money, left_money = user.money, user.money - cost
            if before_money < cost:
                raise error.user_money_not_enough

            ## add new trade record ##
            with tradeDao.transaction():
                # use user coupon
                if coupon_id is not None:
                    tradeDao.use_counpon(coupon_id)

                # add user bill
                tradeDao.add_bill(form.user, before_money, left_money, cost, suite.tpl.bill.margin.item, suite.tpl.bill.margin.detail%(str(margin),))

                # use user money
                tradeDao.use_money(form.user, cost)

                # add trade order record
                code = rand.uuid()
                tradeDao.add_trade(form.user, form.stock, form.coupon, code, form.ptype, form.price, form.count, margin)
                tradeobj = tradeDao.get_trade(code=code)

                # add trade margin record
                tradeDao.add_margin(tradeobj.id, margin, suite.tpl.trademargin.init.item, suite.tpl.trademargin.init.detail%(str(margin),))

                # add trade lever record
                tradeDao.add_lever(tradeobj.id, lever.lever, lever.wline, lever.sline, lever.ofmin, lever.ofrate, lever.dfrate, lever.psrate, lever.mmin, lever.mmax)

                # success #
                self.write(protocol.success(msg=info.msg_buy_success))


class UserSellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.UserSell(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_sell_time(form.ptype, time.time()):
            raise error.not_trading_time

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init trade dao #
            tradeDao = daos.trade.TradeDao(self.db)
            stockDao = daos.stock.StockDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check stock
            stock = stockDao.get(form.stock)
            if stock is None:
                raise error.stock_not_exist

            if stock.status == suite.enum.stock.closed:
                raise error.stock_is_closed

            if stock.status == suite.enum.stock.delisted:
                raise error.stock_is_delisted

            # check free count #
            if not tradeobj.fcount > 0:
                raise error.stock_count_not_enough

            # check price #
            if form.ptype == suite.enum.ptype.xj.code and not rules.trade.valid_sell_price(tradeobj.stock_id, form.price):
                raise error.stock_price_error

            # add new order #
            with tradeDao.transaction():
                # update free count #
                tradeDao.update_trade(tradeobj.id, fcount=0, status=suite.enum.trade.tosell.code)

                # add new order #
                tradeDao.add_order(tradeobj.id, tradeobj.account_id, tradeobj.stock_id,
                                   suite.enum.otype.sell.code, form.ptype, form.price, tradeobj.fcount,
                                   form.operator, suite.enum.oaction.sell.code)

                # success #
                self.write(protocol.success(msg=info.msg_sell_success))


class UserCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.Cancel(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_cancel_time():
            raise error.not_trading_time

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)

            # get order object #
            orderobj = tradeDao.get_order(form.order)
            if orderobj is None:
                raise error.invalid_parameters

            # check trade object #
            tradeobj = tradeDao.get_by_id(orderobj.trade_id)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check order status #
            if suite.enum.order.tocancel.code not in suite.state.order.all.get(form.operator).get(orderobj.status, []):
                raise error.trade_order_cancel_denied

            # append new status log
            logs = suite.status.loads(orderobj.slog)
            otime = int(time.time())
            logs.append(suite.status.format(form.operator, suite.enum.oaction.cancel.code, orderobj.status, suite.enum.order.tocancel.code, otime))
            slog = suite.status.dumps(logs)

            # change order status #
            with tradeDao.transaction():
                # update order #
                tradeDao.update_order(orderobj.id, status=suite.enum.order.tocancel.code, slog=slog, utime=otime)

                # success #
                self.write(protocol.success(msg=info.msg_sell_success))


class CloseHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.Sell(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_close_time(form.ptype, time.time()):
            raise error.not_trading_time

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init trade dao #
            tradeDao = daos.trade.TradeDao(self.db)
            stockDao = daos.stock.StockDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_by_id(form.trade)
            if tradeobj is None or tradeobj.user_id != form.user:
                raise error.invalid_parameters

            # check stock
            stock = stockDao.get(form.stock)
            if stock is None:
                raise error.stock_not_exist

            if stock.status == suite.enum.stock.closed:
                raise error.stock_is_closed

            if stock.status == suite.enum.stock.delisted:
                raise error.stock_is_delisted

            # check hold/free count #
            if tradeobj.fcount != tradeobj.hcount:
                raise error.stock_count_not_match

            # check price #
            if form.ptype == suite.enum.ptype.xj.code and not rules.trade.valid_close_price(tradeobj.stock_id, form.price):
                raise error.stock_price_error

            # add new order #
            with tradeDao.transaction():
                # update free count #
                tradeDao.update_trade(tradeobj.id, fcount=0, status=suite.enum.trade.toclose.code)

                # add new order #
                tradeDao.add_order(tradeobj.id, tradeobj.account_id, tradeobj.stock_id,
                                   suite.enum.otype.close.code, form.ptype, form.price, tradeobj.fcount,
                                   form.operator, suite.enum.oaction.close.code)

                # success #
                self.write(protocol.success(msg=info.msg_sell_success))


class NotifyHandler(handler.Handler):
    """
        notify trade order results
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.Notify(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)

            # get order object #
            orderobj = tradeDao.get_order(form.order)
            if orderobj is None:
                raise error.invalid_parameters

            # check trade object #
            tradeobj = tradeDao.get_by_id(orderobj.trade_id)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check order status #
            if form.status not in suite.state.order.all.get(form.operator).get(orderobj.status, []):
                raise error.trade_order_notify_denied

            # append new order status log
            logs = suite.status.loads(orderobj.slog)
            otime = int(time.time())
            logs.append(suite.status.format(form.operator, suite.enum.oaction.notify.code, orderobj.status, form.status, otime))
            slog = suite.status.dumps(logs)

            isdone, dtime = False, None
            # check if order has done
            if form.dcount + form.ccount == orderobj.ocount:
                isdone = True
                dtime = int(time.time())



            # change order status #
            with tradeDao.transaction():
                # update order #
                tradeDao.update_order(orderobj.id, dcount=form.dcount, dprice=form.dprice, dtime=dtime, status=form.status, slog=slog, utime=otime)

                # update trade #
                if isdone:
                    # trade status log
                    logs = suite.status.loads(tradeobj.slog)
                    otime = int(time.time())

                    if orderobj.otype == suite.enum.otype.buy.code:
                        # to buy complete status log
                        logs.append(suite.status.format(form.operator, suite.enum.oaction.notify.code, tradeobj.status, suite.enum.trade.hold.code, otime))
                        slog = suite.status.dumps(logs)

                        # buy order completed
                        tradeDao.update_trade(tradeobj.id, bcount=form.dcount, bprice=form.dprice, hcount=form.dcount, hprice=form.dprice,
                                              status=suite.enum.trade.hold, slog=slog)
                    elif orderobj.otype == suite.enum.otype.sell.code:
                        # to buy complete status log
                        logs.append(suite.status.format(form.operator, suite.enum.oaction.notify.code, tradeobj.status, suite.enum.trade.sold.code, otime))
                        slog = suite.status.dumps(logs)

                        # sell order completed
                        tradeDao.update_trade(tradeobj.id, scount=form.dcount, sprice=form.sprice, hcount=form.dcount, hprice=form.dprice,
                                              status=suite.enum.trade.sold, slog=slog)
                    elif orderobj.otype == suite.enum.otype.close.code:
                        # close order completed
                        pass
                    else:
                        raise error.order_type_not_exists


                # success #
                self.write(protocol.success(msg=info.msg_notify_success))
