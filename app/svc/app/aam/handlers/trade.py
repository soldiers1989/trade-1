"""
    service admin
"""
import datetime
from app import util
from app.aam import enum, access, handler, daos, forms, models, protocol, myredis, error, log, lock


class AddHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new trade request
        :return:
        """
        ## get arguments ##
        form = forms.trade.Add(**self.arguments)

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

            # check stock count
            if form.count < 100 or form.count%100 != 0:
                raise error.stock_count_error

            # check order price
            if form.price is not None and not util.stock.valid_price(form.stock, form.price):
                raise error.stock_price_error

            # check lever
            lever = leverDao.get(form.lever)
            if lever is None:
                raise error.lever_not_exist

            if lever.disable:
                raise error.lever_has_disabled

            # check coupon
            coupon_money = 0.0
            if form.coupon is not None:
                coupon = couponDao.get(form.coupon)
                if coupon is None:
                    raise error.coupon_not_exist

                if coupon.status != enum.coupon.unused.code:
                    raise error.coupon_has_used

                today = datetime.date.today()
                if today < coupon.sdate or today > coupon.edate:
                    raise error.coupon_has_expired

                coupon_money = coupon.money

            # compute margin
            margin = (form.price * form.count / lever.lever)

            # compute open fee
            ofee = form.price * form.count * lever.ofrate
            ofee = ofee if ofee > lever.ofmin else lever.ofmin

            # check user left money
            left_money = user['money']
            if left_money < margin + ofee - coupon_money:
                raise error.user_money_not_enough

            ## add new trade record ##
            with tradeDao.transaction():
                # change user left money
                #tradeDao.usermoney(form.user, margin+ofee-coupon_money);

                # set user coupon used flag
                #tradeDao.usecoupon(form.coupon)

                # add user bill record


                # add trade order record

                # add trade margin record

                # add trade fee record

                self.write(protocol.success())
