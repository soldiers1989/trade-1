"""
    service admin
"""
import datetime
from app import util
from app.aam import access, handler, models, protocol, redis, error, log, lock


class AddHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new trade request
        :return:
        """

        ## get arguments ##
        userid, couponid, leverid, stockid, price, count = self.get_argument('uid'), self.get_argument('cid', None), self.get_argument('lid'), \
                                                                  self.get_argument('stock'), self.get_argument('price', None), self.get_argument('count')
        ptype = 'xj' if price is not None else 'sj'

        ## process trade add operation by lock user ##
        with lock.user(userid):
            # init trade model #
            tradeModel = models.trade.TradeModel(self.db)

            ## check arguments ##
            # check user
            user = tradeModel.getuser(userid)
            if user is None:
                raise error.user_not_exist

            if user['disable']:
                raise error.user_not_exist

            # check stock
            stock = tradeModel.getstock(stockid)
            if stock is None:
                raise error.stock_not_exist

            if stock['status'] == 'close':
                raise error.stock_is_closed

            if stock['status'] == 'delisted':
                raise error.stock_is_delisted

            if stock['limit'] == 'nobuy' or stock['limit'] == 'nodelay':
                raise error.stock_buy_limited

            # check stock count
            if count < 100 or count%100 != 0:
                raise error.stock_count_error

            # check order price
            if price is not None and not util.stock.valid_price(stockid, price):
                raise error.stock_price_error

            # check lever
            lever = tradeModel.getlever(leverid)
            if lever is None:
                raise error.lever_not_exist

            if lever['disable']:
                raise error.lever_has_disabled

            # check coupon
            coupon_money = 0.0
            if couponid is not None:
                coupon = tradeModel.getcoupon(couponid)
                if coupon is None:
                    raise error.coupon_not_exist

                if coupon['status'] != 'unused':
                    raise error.coupon_has_used

                today = datetime.date.today()
                if today < coupon['sdate'] or today > coupon['edate']:
                    raise error.coupon_has_expired

                coupon_money = coupon['money']

            # compute margin
            margin = (price * count / lever['lever'])

            # compute open fee
            ofee = price * count * lever['ofrate']
            ofee = ofee if ofee > lever['ofmin'] else lever['ofmin']

            # check user left money
            left_money = user['money']
            if left_money < margin + ofee - coupon_money:
                raise error.user_money_not_enough

            ## add new trade record ##
            tradeModel.dbbegin()

            # change user left money
            tradeModel.usermoney(userid, margin+ofee-coupon_money);

            # set user coupon used flag
            tradeModel.usecoupon(couponid)

            # add user bill record

            # add trade order record

            # add trade margin record

            # add trade fee record

            tradeModel.dbcommit()

            self.write(protocol.success())
