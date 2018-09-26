"""
    trade management
"""
import datetime, decimal, time

from tlib import rand
from .. import suite, daos, error, lock, trade, mysql, forms


def get_trades(**conds):
    """
        get trade records
    :param conds:
    :return:
    """
    # connect database
    db = mysql.get()

    # init dao object
    dao = daos.trade.TradeDao(db)

    # get records
    results = dao.get_trades(**conds)

    return results


def user_buy(form):
    """
        process user buy
    :param form: obj, forms.trade.UserBuy
    :return:
        trade order object
    """
    ## check trade time ##
    if not trade.rule.valid_user_buy_time(form.ptype):
        raise error.not_trading_time

    ## process trade add operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init trade dao #
        tradeDao = daos.trade.TradeDao(db)
        userDao = daos.user.UserDao(db)
        stockDao = daos.stock.StockDao(db)
        leverDao = daos.lever.LeverDao(db)
        couponDao = daos.coupon.CouponDao(db)

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
        if not trade.rule.valid_user_buy_count(form.count):
            raise error.stock_count_error

        # check order price
        if form.price is None or not trade.rule.valid_user_buy_price(form.stock, form.price):
            raise error.stock_price_error

        # check capital
        capital = form.price * form.count

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
            return tradeobj


def user_sell(form):
    """
        process user sell
    :param form: obj, forms.trade.UserSell
    :return:
        trade object
    """
    ## check trade time ##
    if not trade.rule.valid_user_sell_time(form.ptype):
        raise error.not_trading_time

    ## process trade sell operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init trade dao #
        tradeDao = daos.trade.TradeDao(db)
        stockDao = daos.stock.StockDao(db)

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
        if form.ptype == suite.enum.ptype.xj.code and not trade.rule.valid_user_sell_price(tradeobj.stock_id, form.price):
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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def user_close(form):
    """
       process user close(系统调用平仓)
    :param form: obj, forms.trade.UserClose
    :return:
        trade object
    """
    ## check trade time ##
    if not trade.rule.valid_user_close_time(form.ptype):
        raise error.not_trading_time

    ## process trade sell operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init trade dao #
        tradeDao = daos.trade.TradeDao(db)
        stockDao = daos.stock.StockDao(db)

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
        if form.ptype == suite.enum.ptype.xj.code and not trade.rule.valid_user_close_price(tradeobj.stock_id, form.price):
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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def user_cancel(form):
    """
        process user cancel
    :param form: obj, forms.trade.UserCancel
    :return:
        trade object
    """
    ## check trade time ##
    if not trade.rule.valid_user_cancel_time():
        raise error.not_trading_time

    ## process trade sell operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init dao #
        tradeDao = daos.trade.TradeDao(db)
        userDao = daos.user.UserDao(db)

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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_buy(form):
    """
        process system buy
    :param form: obj, forms.trade.SysBuy
    :return:
        trade object
    """
    ## process trade operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init trade dao #
        tradeDao = daos.trade.TradeDao(db)
        stockDao = daos.stock.StockDao(db)

        # check trade object #
        tradeobj = tradeDao.get_trade(id=form.trade)
        if tradeobj is None or form.user != tradeobj.user_id:
            raise error.invalid_parameters

        ## check trade time ##
        if not trade.rule.valid_sys_buy_time(tradeobj.optype):
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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_sell(form):
    """
        process system sell
    :param form: obj, forms.trade.SysSell
    :return:
        trade object
    """
    ## process trade operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init trade dao #
        tradeDao = daos.trade.TradeDao(db)
        stockDao = daos.stock.StockDao(db)

        # check trade object #
        tradeobj = tradeDao.get_trade(id=form.trade)
        if tradeobj is None or form.user != tradeobj.user_id:
            raise error.invalid_parameters

        ## check trade time ##
        if not trade.rule.valid_sys_sell_time(tradeobj.optype):
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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_close(form):
    """
        process system close
    :param form: obj, forms.trade.SysClose
    :return:
        trade object
    """
    ## check trade time ##
    if not trade.rule.valid_sys_close_time(form.ptype, time.time()):
        raise error.not_trading_time

    ## process trade sell operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init trade dao #
        tradeDao = daos.trade.TradeDao(db)

        # check trade object #
        tradeobj = tradeDao.get_trade(id=form.trade)
        if tradeobj is None or tradeobj.user_id != form.user:
            raise error.invalid_parameters

        # check current trade status
        if tradeobj.status != suite.enum.trade.toclose.code:
            raise error.trade_operation_denied

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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_cancel(form):
    """
        process system cancel
    :param form: obj, forms.trade.SysCancel
    :return:
        trade object
    """
    ## check trade time ##
    if not trade.rule.valid_user_cancel_time():
        raise error.not_trading_time

    ## process trade sell operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init dao #
        tradeDao = daos.trade.TradeDao(db)

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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_bought(form):
    """
        process system bought
    :param form: obj, forms.trade.SysBought
    :return:
        trade object
    """
    ## process trade operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init dao #
        tradeDao = daos.trade.TradeDao(db)

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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_sold(form):
    """
        process system sold
    :param form: obj, forms.trade.SysSold
    :return:
        trade object
    """
    ## process trade operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init dao #
        tradeDao = daos.trade.TradeDao(db)
        userDao = daos.user.UserDao(db)

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
                                      utime=int(time.time()), stime=int(time.time()), etime=int(time.time()))

                # add user bill
                tradeDao.add_bill(tradeobj.user_id, bmoney, lmoney, money,
                                  suite.tpl.bill.profit.item,
                                  suite.tpl.bill.profit.detail%(str(money)))

                # update user left money
                tradeDao.update_money(userobj.id, lmoney)

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_closed(form):
    """
        process system closed
    :param form: obj, forms.trade.SysClosed
    :return:
        trade object
    """
    ## process trade operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init dao #
        tradeDao = daos.trade.TradeDao(db)
        userDao = daos.user.UserDao(db)

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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_canceled(form, expired = False):
    """
        process system canceled
    :param form: obj, forms.trade.SysCanceled
    :return:
        trade object
    """
    ## process trade operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init dao #
        tradeDao = daos.trade.TradeDao(db)
        userDao = daos.user.UserDao(db)

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
            if not expired:
                next_status = suite.enum.trade.canceled.code
            else:
                next_status = suite.enum.trade.expired.code
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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def sys_dropped(form):
    """
        process system dropped
    :param form: obj, forms.trade.SysDropped
    :return:
        trade object
    """
    ## process trade operation by lock user ##
    with lock.user(form.user):
        # connect database #
        db = mysql.get()

        # init dao #
        tradeDao = daos.trade.TradeDao(db)
        userDao = daos.user.UserDao(db)

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

            # get new tradeobj
            tradeobj = tradeDao.get_trade(id=form.trade)

            # success #
            return tradeobj


def trade_notify(form):
    """
        process order notify
    :param form: obj, forms.trade.TradeNotify
    :return:
        trade object
    """
    # connect database
    db = mysql.get()

    # init dao
    tradeDao = daos.trade.TradeDao(db)

    # get trade object
    tradeobj = tradeDao.get_trade(code=form.code)

    # order data
    user, trade,  = tradeobj.user_id, tradeobj.id
    otype, dcount, dprice, status = form.otype, form.dcount, form.dprice, form.status

    # process trade operation by lock user
    with lock.user(user):
        if status in [suite.enum.order.tdeal, suite.enum.order.pdeal, suite.enum.order.pcanceled]:
            # total dealt / part dealt
            if otype in [suite.enum.otype.buy]:
                return sys_bought(forms.trade.SysBought(user=user, trade=trade, count=dcount, price=dprice))
            elif otype in [suite.enum.otype.sell, suite.enum.otype.close]:
                return sys_sold(forms.trade.SysBought(user=user, trade=trade, count=dcount, price=dprice))
            else:
                raise error.invalid_parameters
        elif status in [suite.enum.order.tcanceled]:
            # total canceled
            if otype in [suite.enum.otype.buy, suite.enum.otype.sell, suite.enum.otype.close]:
                return sys_canceled(forms.trade.SysCanceled(user=user, trade=trade))
            else:
                raise error.invalid_parameters
        elif status in [suite.enum.order.expired]:
            # expired
            if otype in [suite.enum.otype.buy, suite.enum.otype.sell, suite.enum.otype.close]:
                return sys_canceled(forms.trade.SysCanceled(user=user, trade=trade), expired=True)
            else:
                raise error.invalid_parameters
        else:
            raise error.invalid_parameters

