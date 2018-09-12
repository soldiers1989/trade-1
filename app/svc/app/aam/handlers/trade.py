"""
    trade management
"""
import datetime
import decimal
import time

from tlib import rand
from .. import suite, access, handler, daos, forms, protocol, error, info, lock, rules


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
        if not rules.trade.valid_user_buy_time(form.ptype):
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
            if not rules.trade.valid_user_buy_count(form.count):
                raise error.stock_count_error

            # check order price
            if form.price is None or not rules.trade.valid_user_buy_price(form.stock, form.price):
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
            coupon_id, coupon_money = None, decimal.Decimal('0.00')
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
                tradeDao.add_bill(form.user, before_money, left_money, cost, suite.tpl.bill.tmargin.item, suite.tpl.bill.tmargin.detail%(str(margin),))

                # use user money
                tradeDao.update_money(form.user, left_money)

                # add trade order record
                code = rand.uuid()
                tradeDao.add_trade(form.user, form.stock, form.coupon, code, form.ptype, form.price, form.count, margin)
                tradeobj = tradeDao.get_trade(code=code)

                # add trade margin record
                tradeDao.add_margin(tradeobj.id, margin, suite.tpl.trademargin.init.item, suite.tpl.trademargin.init.detail%(str(margin),))

                # add trade lever record
                tradeDao.add_lever(tradeobj.id, lever.lever, lever.wline, lever.sline, lever.ofmin, lever.ofrate, lever.dfrate, lever.psrate, lever.mmin, lever.mmax)

                # success #
                self.write(protocol.success(msg=info.msg_user_buy_success, data={'trade': tradeobj.id}))


class UserSellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.UserSell(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_user_sell_time(form.ptype):
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

            # check current trade status
            if tradeobj.status != suite.enum.trade.hold.code:
                raise error.trade_operation_denied

            # check stock
            stock = stockDao.get(id=tradeobj.stock_id)
            if stock is None:
                raise error.stock_not_exist

            if stock.status == suite.enum.stock.closed:
                raise error.stock_is_closed

            if stock.status == suite.enum.stock.delisted:
                raise error.stock_is_delisted

            # check free count /hold count #
            if not tradeobj.fcount > 0 :
                raise error.stock_count_not_enough
            if tradeobj.hcount != tradeobj.fcount:
                raise error.stock_count_not_match

            # check price #
            if form.ptype == suite.enum.ptype.xj.code and not rules.trade.valid_user_sell_price(tradeobj.stock_id, form.price):
                raise error.stock_price_error

            # prepare status log
            logs = suite.status.trade.loads(tradeobj.slog)
            time_now = int(time.time())
            logs.append(suite.status.trade.format(suite.enum.operator.user.code,
                                                  suite.enum.oaction.sell.code,
                                                  form.ptype,
                                                  str(form.price),
                                                  tradeobj.fcount,
                                                  tradeobj.status,
                                                  suite.enum.trade.tosell.code,
                                                  time_now))
            slog = suite.status.trade.dumps(logs)

            # add new order #
            with tradeDao.transaction():
                # update free count #
                tradeDao.update_trade(tradeobj.id, optype=form.ptype, oprice=form.price, ocount=tradeobj.fcount, fcount=0,
                                      status=suite.enum.trade.tosell.code, slog=slog,
                                      utime=time_now, ostime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_user_sell_success, data={'trade': tradeobj.id}))


class UserCloseHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.UserClose(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_user_close_time(form.ptype):
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

            # check current trade status
            if tradeobj.status != suite.enum.trade.hold.code:
                raise error.trade_operation_denied

            # check stock
            stock = stockDao.get(id=tradeobj.stock_id)
            if stock is None:
                raise error.stock_not_exist
            if stock.status == suite.enum.stock.closed:
                raise error.stock_is_closed
            if stock.status == suite.enum.stock.delisted:
                raise error.stock_is_delisted

            # check free count /hold count #
            if not tradeobj.fcount > 0 :
                raise error.stock_count_not_enough
            if tradeobj.hcount != tradeobj.fcount:
                raise error.stock_count_not_match

            # check price #
            if form.ptype == suite.enum.ptype.xj.code and not rules.trade.valid_user_close_price(tradeobj.stock_id, form.price):
                raise error.stock_price_error

            # prepare status log
            logs = suite.status.trade.loads(tradeobj.slog)
            time_now = int(time.time())
            logs.append(suite.status.trade.format(suite.enum.operator.user.code,
                                                  suite.enum.oaction.close.code,
                                                  form.ptype,
                                                  str(form.price),
                                                  tradeobj.fcount,
                                                  tradeobj.status,
                                                  suite.enum.trade.toclose.code,
                                                  time_now))
            slog = suite.status.trade.dumps(logs)

            # add new order #
            with tradeDao.transaction():
                # update free count #
                tradeDao.update_trade(tradeobj.id, optype=form.ptype, oprice=form.price, ocount=tradeobj.fcount, fcount=0,
                                      status=suite.enum.trade.toclose.code, slog=slog,
                                      utime=time_now, stime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_user_close_success, data={'trade': tradeobj.id}))


class UserCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.UserCancel(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_user_cancel_time():
            raise error.not_trading_time

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)
            userDao = daos.user.UserDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check user object #
            userobj = userDao.get(id=form.user)
            if userobj is None:
                raise error.invalid_parameters

            next_status = None
            # check trade status #
            if tradeobj.status in [suite.enum.trade.tobuy.code]:
                next_status = suite.enum.trade.canceled.code
            elif tradeobj.status in [suite.enum.trade.buying.code]:
                next_status = suite.enum.trade.cancelbuy.code
            elif tradeobj.status in [suite.enum.trade.tosell.code]:
                next_status = suite.enum.trade.hold.code
            elif tradeobj.status in [suite.enum.trade.selling.code]:
                next_status = suite.enum.trade.cancelsell.code
            elif tradeobj.status in [suite.enum.trade.toclose.code]:
                next_status = suite.enum.trade.hold.code
            elif tradeobj.status in [suite.enum.trade.closing.code]:
                next_status = suite.enum.trade.cancelclose.code
            else:
                raise error.trade_operation_denied

            # append new status log
            logs = suite.status.trade.loads(tradeobj.slog)
            time_now = int(time.time())
            logs.append(suite.status.trade.format(suite.enum.operator.user.code,
                                            suite.enum.oaction.cancel.code,
                                            tradeobj.optype,
                                            str(tradeobj.oprice),
                                            tradeobj.ocount,
                                            tradeobj.status,
                                            next_status,
                                            time_now))
            slog = suite.status.trade.dumps(logs)

            # change order status #
            with tradeDao.transaction():
                if next_status == suite.enum.trade.hold.code:
                    # tosell/toclose->hold #
                    tradeDao.update_trade(tradeobj.id, status=next_status, slog=slog, utime=time_now)
                else:
                    # tobuy->canceled, return margin #
                    # by canceled, need return margin #
                    tradeDao.update_trade(tradeobj.id,
                                          status=next_status, slog=slog,
                                          utime=int(time.time()), etime=time_now)

                    # add bill
                    money = tradeobj.margin
                    bmoney, lmoney = userobj.money, userobj.money+money
                    tradeDao.add_bill(tradeobj.user_id, bmoney, lmoney, money,
                                      suite.tpl.bill.rmargin.item,
                                      suite.tpl.bill.rmargin.detail%(str(money)))

                    # return margin
                    tradeDao.update_money(tradeobj.user_id, lmoney)

                # success #
                self.write(protocol.success(msg=info.msg_user_cancel_success, data={'trade': tradeobj.id}))


class SysBuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.SysBuy(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init trade dao #
            tradeDao = daos.trade.TradeDao(self.db)
            stockDao = daos.stock.StockDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            ## check trade time ##
            if not rules.trade.valid_sys_buy_time(tradeobj.optype):
                raise error.not_trading_time

            # check current trade status
            if tradeobj.status != suite.enum.trade.tobuy.code:
                raise error.trade_operation_denied

            # check stock
            stock = stockDao.get(id=tradeobj.stock_id)
            if stock is None:
                raise error.stock_not_exist
            if stock.status == suite.enum.stock.closed:
                raise error.stock_is_closed
            if stock.status == suite.enum.stock.delisted:
                raise error.stock_is_delisted
            if stock.limit == suite.enum.risk.nobuy or stock.limit == suite.enum.risk.nodelay:
                raise error.stock_buy_limited

            # prepare status log
            logs = suite.status.trade.loads(tradeobj.slog)
            time_now = int(time.time())
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.buy.code,
                                                  tradeobj.optype,
                                                  str(tradeobj.oprice),
                                                  tradeobj.ocount,
                                                  tradeobj.status,
                                                  suite.enum.trade.buying.code,
                                                  time_now))
            slog = suite.status.trade.dumps(logs)

            # add new order #
            with tradeDao.transaction():
                # update free count #
                tradeDao.update_trade(tradeobj.id, status=suite.enum.trade.buying.code, slog=slog, utime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_sys_buy_success, data={'trade': tradeobj.id}))


class SysSellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.SysSell(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init trade dao #
            tradeDao = daos.trade.TradeDao(self.db)
            stockDao = daos.stock.StockDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            ## check trade time ##
            if not rules.trade.valid_sys_sell_time(tradeobj.optype):
                raise error.not_trading_time

            # check current trade status
            if tradeobj.status != suite.enum.trade.tosell.code:
                raise error.trade_operation_denied

            # check stock
            stock = stockDao.get(id=tradeobj.stock_id)
            if stock is None:
                raise error.stock_not_exist
            if stock.status == suite.enum.stock.closed:
                raise error.stock_is_closed
            if stock.status == suite.enum.stock.delisted:
                raise error.stock_is_delisted

            # prepare status log
            logs = suite.status.trade.loads(tradeobj.slog)
            time_now = int(time.time())
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.sell.code,
                                                  tradeobj.optype,
                                                  str(tradeobj.oprice),
                                                  tradeobj.ocount,
                                                  tradeobj.status,
                                                  suite.enum.trade.selling.code,
                                                  time_now))
            slog = suite.status.trade.dumps(logs)

            # add new order #
            with tradeDao.transaction():
                # update free count #
                tradeDao.update_trade(tradeobj.id, status=suite.enum.trade.buying.code, slog=slog, utime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_sys_sell_success, data={'trade': tradeobj.id}))


class SysCloseHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.SysClose(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_sys_close_time(form.ptype, time.time()):
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

            # prepare status log
            logs = suite.status.trade.loads(tradeobj.slog)
            time_now = int(time.time())
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.close.code,
                                                  tradeobj.optype,
                                                  str(tradeobj.oprice),
                                                  tradeobj.ocount,
                                                  tradeobj.status,
                                                  suite.enum.trade.closing.code,
                                                  time_now))
            slog = suite.status.trade.dumps(logs)

            # add new order #
            with tradeDao.transaction():
                # update free count #
                tradeDao.update_trade(tradeobj.id,  status=suite.enum.trade.closing.code, slog=slog, utime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_sys_close_success, data={'trade': tradeobj.id}))


class SysCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.UserCancel(**self.arguments)

        ## check trade time ##
        if not rules.trade.valid_user_cancel_time():
            raise error.not_trading_time

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            next_status = None
            # check trade status #
            if tradeobj.status in [suite.enum.trade.cancelbuy.code]:
                next_status = suite.enum.trade.buycanceling.code
            elif tradeobj.status in [suite.enum.trade.cancelsell.code]:
                next_status = suite.enum.trade.sellcanceling.code
            elif tradeobj.st in [suite.enum.trade.cancelclose.code]:
                next_status = suite.enum.trade.closecanceling.code
            else:
                raise error.trade_operation_denied

            # append new status log
            logs = suite.status.trade.loads(tradeobj.slog)
            time_now = int(time.time())
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.cancel.code,
                                                  tradeobj.optype,
                                                  str(tradeobj.oprice),
                                                  tradeobj.ocount,
                                                  tradeobj.status,
                                                  next_status,
                                                  time_now))
            slog = suite.status.trade.dumps(logs)

            # change order status #
            with tradeDao.transaction():
                # update order #
                tradeDao.update_trade(tradeobj.id, status=next_status, slog=slog, utime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_sys_cancel_success, data={'trade': tradeobj.id}))


class SysBoughtHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.SysBought(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check lever object #
            leverobj = tradeDao.get_lever(form.trade)
            if leverobj is None:
                raise error.server_exception

            next_status = suite.enum.trade.hold.code
            # trade status must be[tobuy, buying, cancelbuy, buycanceling]#
            if tradeobj.status not in [suite.enum.trade.tobuy.code,
                                       suite.enum.trade.buying.code,
                                       suite.enum.trade.cancelbuy.code,
                                       suite.enum.trade.buycanceling.code]:
                raise error.trade_operation_denied

            # compute open fee
            ofee = max(leverobj.ofmin, leverobj.ofrate*form.count*form.price)

            # append new status log
            logs = suite.status.trade.loads(tradeobj.slog)
            time_now = int(time.time())
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.buy.code,
                                                  tradeobj.optype,
                                                  str(form.price),
                                                  form.count,
                                                  tradeobj.status,
                                                  next_status,
                                                  time_now))
            slog = suite.status.trade.dumps(logs)

            # change order status #
            with tradeDao.transaction():
                # update order #
                tradeDao.update_trade(tradeobj.id, hprice=form.price, hcount=form.count, fcount=form.count,
                                      bprice=form.price, bcount=form.count,
                                      ofee=ofee, status=next_status, slog=slog,
                                      utime=time_now, btime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_sys_bought_success, data={'trade': tradeobj.id}))


class SysSoldHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.SysSold(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)
            userDao = daos.user.UserDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check lever object #
            leverobj = tradeDao.get_lever(form.trade)
            if leverobj is None:
                raise error.server_exception

            # check user object #
            userobj = userDao.get(id=form.user)
            if userobj is None:
                raise error.invalid_parameters


            # trade status must be[tobuy, buying, cancelbuy, buycanceling]#
            if tradeobj.status not in [suite.enum.trade.tosell.code,
                                       suite.enum.trade.selling.code,
                                       suite.enum.trade.cancelsell.code,
                                       suite.enum.trade.sellcanceling.code]:
                raise error.trade_operation_denied

            # process hold count/status
            hcount, next_status = tradeobj.hcount - form.count, None
            if hcount > 0:
                next_status = suite.enum.trade.hold.code
            elif hcount == 0:
                next_status = suite.enum.trade.sold.code
            else:
                raise error.sold_count_not_match

            # process sold count/price
            scount, sprice = 0 if tradeobj.scount is None else tradeobj.scount, decimal.Decimal('0.00') if tradeobj.sprice is None else tradeobj.sprice
            sprice = (form.count*form.price + scount*sprice)/(scount+form.count)
            scount = scount + form.count

            # append new status log
            logs = suite.status.trade.loads(tradeobj.slog)
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.sell.code,
                                                  tradeobj.optype,
                                                  str(form.price),
                                                  form.count,
                                                  tradeobj.status,
                                                  next_status,
                                                  int(time.time())))
            slog = suite.status.trade.dumps(logs)

            # change order status #
            with tradeDao.transaction():
                if next_status != suite.enum.trade.sold.code:
                    # trade not completed #
                    tradeDao.update_trade(tradeobj.id, hcount=hcount,
                                          sprice=sprice, scount=scount,
                                          status=next_status, slog=slog,
                                          utime=int(time.time()))
                else:
                    # trade has completed #
                    ofee, dfee, margin = tradeobj.ofee, tradeobj.dfee, tradeobj.margin
                    tprofit = scount * sprice - tradeobj.bcount * tradeobj.bprice
                    sprofit = max(decimal.Decimal('0.00'), tprofit * leverobj.psrate)

                    # money for settlement#
                    money = tprofit + margin - sprofit - ofee - dfee
                    bmoney = userobj.money
                    lmoney = userobj.money + money

                    # update trade record
                    tradeDao.update_trade(tradeobj.id, hcount=hcount,
                                          sprice=sprice, scount=scount,
                                          tprofit=tprofit, sprofit=sprofit,
                                          status=next_status, slog=slog,
                                          utime=int(time.time()), stime=int(time.time(), etime=int(time.time())))

                    # add user bill
                    tradeDao.add_bill(tradeobj.user_id, bmoney, lmoney, money,
                                      suite.tpl.bill.profit.item,
                                      suite.tpl.bill.profit.detail%(str(money)))

                    # update user left money
                    tradeDao.update_money(userobj.id, lmoney)

                # success #
                self.write(protocol.success(msg=info.msg_sys_sold_success, data={'trade': tradeobj.id}))


class SysClosedHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.SysClosed(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)
            userDao = daos.user.UserDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check lever object #
            leverobj = tradeDao.get_lever(form.trade)
            if leverobj is None:
                raise error.server_exception

            # check user object #
            userobj = userDao.get(id=form.user)
            if userobj is None:
                raise error.invalid_parameters


            # trade status must be[toclose, closing, cancelclose, closecanceling]#
            if tradeobj.status not in [suite.enum.trade.toclose.code,
                                       suite.enum.trade.closing.code,
                                       suite.enum.trade.cancelclose.code,
                                       suite.enum.trade.closecanceling.code]:
                raise error.trade_operation_denied

            # process hold count/status
            hcount, next_status = tradeobj.hcount - form.count, None
            if hcount > 0:
                next_status = suite.enum.trade.hold.code
            elif hcount == 0:
                next_status = suite.enum.trade.closed.code
            else:
                raise error.sold_count_not_match

            # process sold count/price
            scount, sprice = 0 if tradeobj.scount is None else tradeobj.scount, decimal.Decimal('0.00') if tradeobj.sprice is None else tradeobj.sprice
            sprice = (form.count*form.price + scount*sprice)/(scount+form.count)
            scount = scount + form.count

            # append new status log
            logs = suite.status.trade.loads(tradeobj.slog)
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.close.code,
                                                  tradeobj.optype,
                                                  str(form.price),
                                                  form.count,
                                                  tradeobj.status,
                                                  next_status,
                                                  int(time.time())))
            slog = suite.status.trade.dumps(logs)

            # change order status #
            with tradeDao.transaction():
                if next_status != suite.enum.trade.sold.code:
                    # trade not completed #
                    tradeDao.update_trade(tradeobj.id, hcount=hcount,
                                          sprice=sprice, scount=scount,
                                          status=next_status, slog=slog,
                                          utime=int(time.time()))
                else:
                    # trade has completed #
                    ofee, dfee, margin = tradeobj.ofee, tradeobj.dfee, tradeobj.margin
                    tprofit = scount * sprice - tradeobj.bcount * tradeobj.bprice
                    sprofit = max(decimal.Decimal('0.00'), tprofit * leverobj.psrate)

                    # money for settlement#
                    money = tprofit + margin - sprofit - ofee - dfee
                    bmoney = userobj.money
                    lmoney = userobj.money + money

                    # update trade record
                    tradeDao.update_trade(tradeobj.id, hcount=hcount,
                                          sprice=sprice, scount=scount,
                                          tprofit=tprofit, sprofit=sprofit,
                                          status=next_status, slog=slog,
                                          utime=int(time.time()), stime=int(time.time()), etime=int(time.time()))

                    # add user bill
                    tradeDao.add_bill(tradeobj.user_id, bmoney, lmoney, money,
                                      suite.tpl.bill.profit.item,
                                      suite.tpl.bill.profit.detail%(str(money)))

                    # update user left money
                    tradeDao.update_money(userobj.id, lmoney)

                # success #
                self.write(protocol.success(msg=info.msg_sys_closed_success, data={'trade': tradeobj.id}))


class SysCanceledHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.SysCanceled(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)
            userDao = daos.user.UserDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check user object #
            userobj = userDao.get(id=form.user)
            if userobj is None:
                raise error.invalid_parameters

            next_status, etime = None, None
            # check trade status #
            if tradeobj.status in [suite.enum.trade.cancelbuy.code, suite.enum.trade.buycanceling.code]:
                etime = int(time.time())
                next_status = suite.enum.trade.canceled.code
            elif tradeobj.status in [suite.enum.trade.cancelsell.code, suite.enum.trade.sellcanceling.code,
                                     suite.enum.trade.cancelclose.code, suite.enum.trade.closecanceling.code]:
                next_status = suite.enum.trade.hold.code
            else:
                raise error.trade_operation_denied

            # append new status log
            logs = suite.status.trade.loads(tradeobj.slog)
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.cancel.code,
                                                  tradeobj.optype,
                                                  str(tradeobj.oprice),
                                                  tradeobj.ocount,
                                                  tradeobj.status,
                                                  next_status,
                                                  time.time()))
            slog = suite.status.trade.dumps(logs)

            # change order status #
            with tradeDao.transaction():
                if next_status == suite.enum.trade.hold.code:
                    # sell/close canceled, just update free count #
                    tradeDao.update_trade(tradeobj.id, fcount=tradeobj.hcount,
                                          status=next_status, slog=slog,
                                          utime=int(time.time()), etime=etime)
                else:
                    # by canceled, need return margin #
                    tradeDao.update_trade(tradeobj.id,
                                          status=next_status, slog=slog,
                                          utime=int(time.time()), etime=etime)

                    # add bill
                    money = tradeobj.margin
                    bmoney, lmoney = userobj.money, userobj.money+money
                    tradeDao.add_bill(tradeobj.user_id, bmoney, lmoney, money,
                                      suite.tpl.bill.rmargin.item,
                                      suite.tpl.bill.rmargin.detail%(str(money)))

                    # return margin
                    tradeDao.update_money(tradeobj.user_id, lmoney)

                # success #
                self.write(protocol.success(msg=info.msg_sys_canceled_success, data={'trade': tradeobj.id}))


class SysDroppedHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.SysDropped(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init dao #
            tradeDao = daos.trade.TradeDao(self.db)
            userDao = daos.user.UserDao(self.db)

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            # check user object #
            userobj = userDao.get(id=form.user)
            if userobj is None:
                raise error.invalid_parameters

            # check trade status #
            if tradeobj.status not in [suite.enum.trade.tobuy.code]:
                raise error.trade_operation_denied

            next_status, etime = suite.enum.trade.dropped.code, int(time.time())
            # append new status log
            logs = suite.status.trade.loads(tradeobj.slog)
            logs.append(suite.status.trade.format(suite.enum.operator.sys.code,
                                                  suite.enum.oaction.drop.code,
                                                  tradeobj.optype,
                                                  str(tradeobj.oprice),
                                                  tradeobj.ocount,
                                                  tradeobj.status,
                                                  next_status,
                                                  etime))
            slog = suite.status.trade.dumps(logs)

            # change order status #
            with tradeDao.transaction():
                # return margin #
                tradeDao.update_trade(tradeobj.id,
                                      status=next_status, slog=slog,
                                      utime=etime, etime=etime)

                # add bill
                money = tradeobj.margin
                bmoney, lmoney = userobj.money, userobj.money+money
                tradeDao.add_bill(tradeobj.user_id, bmoney, lmoney, money,
                                  suite.tpl.bill.rmargin.item,
                                  suite.tpl.bill.rmargin.detail%(str(money)))

                # return margin
                tradeDao.update_money(tradeobj.user_id, lmoney)

                # success #
                self.write(protocol.success(msg=info.msg_sys_canceled_success, data={'trade': tradeobj.id}))