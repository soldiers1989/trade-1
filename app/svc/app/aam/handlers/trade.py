"""
    service admin
"""
import datetime
from app import rules
from app.util import rand
from app.aam import enum, access, handler, daos, forms, protocol, error, lock, tpl


class BuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new trade request
        :return:
        """
        ## get arguments ##
        form = forms.trade.Buy(**self.arguments)

        ## process trade add operation by lock user ##
        with lock.user(form.user):
            # init trade dao #
            tradeDao = daos.trade.TradeDao(self.db)
            userDao = daos.user.UserDao(self.db)
            stockDao = daos.stock.StockDao(self.db)
            leverDao = daos.lever.LeverDao(self.db)
            couponDao = daos.coupon.CouponDao(self.db)

            ## check arguments ##
            # check user
            user = userDao.get(form.user)
            if user is None:
                raise error.user_not_exist

            if user.disable:
                raise error.user_not_exist

            # check stock
            stock = stockDao.get(form.stock)
            if stock is None:
                raise error.stock_not_exist

            if stock.status == enum.stock.closed:
                raise error.stock_is_closed

            if stock.status == enum.stock.delisted:
                raise error.stock_is_delisted

            if stock.limit == enum.risk.nobuy or stock.limit == enum.risk.nodelay:
                raise error.stock_buy_limited

            # check lever
            lever = leverDao.get(form.lever)
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

            capital = form.price * form.count
            # check lever money limit
            if capital > lever.mmax or capital< lever.mmin:
                raise error.lever_capital_denied

            # check coupon
            coupon_id, coupon_money = None, 0.0
            if form.coupon is not None:
                coupon = couponDao.get(form.coupon)
                if coupon is None:
                    raise error.coupon_not_exist

                if coupon.user_id != form.user:
                    raise error.invalid_parameters

                if coupon.status != enum.coupon.unused.code:
                    raise error.coupon_has_used

                today = datetime.date.today()
                if today < coupon.sdate or today > coupon.edate:
                    raise error.coupon_has_expired

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
                tradeDao.add_bill(form.user, before_money, left_money, cost, tpl.bill.margin.item, tpl.bill.margin.detail%(str(margin),))

                # use user money
                tradeDao.use_money(form.user, cost)

                # add trade order record
                code = rand.uuid()
                tradeDao.add_trade(form.user, form.stock, form.coupon, code, form.ptype, form.price, form.count, margin)
                tradeobj = tradeDao.get_by_code(code)

                # add trade margin record
                tradeDao.add_margin(tradeobj.id, margin, tpl.trademargin.init.item, tpl.trademargin.init.detail%(str(margin),))

                # add trade lever record
                tradeDao.add_lever(tradeobj.id, lever.lever, lever.wline, lever.sline, lever.ofmin, lever.ofrate, lever.dfrate, lever.psrate, lever.mmin, lever.mmax)

                self.write(protocol.success())


class SellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        ## get arguments ##
        form = forms.trade.Sell(**self.arguments)

        ## process trade sell operation by lock user ##
        with lock.user(form.user):
            # init trade dao #
            tradeDao = daos.trade.TradeDao(self.db)


class CloseHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        pass


class CancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        pass

