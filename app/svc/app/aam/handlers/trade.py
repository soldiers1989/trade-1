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
                tradeDao.update_trade(tradeobj.id, optype=form.ptype, oprice=form.price, ocount=tradeobj.fcount, fcount=0, status=suite.enum.trade.tosell.code, slog=slog, utime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_sell_success))


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
                tradeDao.update_trade(tradeobj.id, optype=form.ptype, oprice=form.price, ocount=tradeobj.fcount, fcount=0, status=suite.enum.trade.toclose.code, slog=slog, utime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_sell_success))


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

            # check trade object #
            tradeobj = tradeDao.get_trade(id=form.trade)
            if tradeobj is None or form.user != tradeobj.user_id:
                raise error.invalid_parameters

            next_status = None
            # check trade status #
            if tradeobj.status in [suite.enum.trade.tobuy.code, suite.enum.trade.buying.code]:
                next_status = suite.enum.trade.cancelbuy.code
            elif tradeobj.status in [suite.enum.trade.tosell.code, suite.enum.trade.selling.code]:
                next_status = suite.enum.trade.cancelsell.code
            elif tradeobj.status in [suite.enum.trade.toclose.code, suite.enum.trade.closing.code]:
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
                # update order #
                tradeDao.update_trade(tradeobj.id, status=next_status, slog=slog, utime=time_now)

                # success #
                self.write(protocol.success(msg=info.msg_cancel_success))


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
                self.write(protocol.success(msg=info.msg_sell_success))


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
                self.write(protocol.success(msg=info.msg_sell_success))


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
                self.write(protocol.success(msg=info.msg_sell_success))


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
                self.write(protocol.success(msg=info.msg_cancel_success))
