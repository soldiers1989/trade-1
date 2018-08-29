"""
    service admin
"""
from app.aam import access, handler, models, protocol, redis, error, log


class AddHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new trade request
        :return:
        """

        # get arguments
        userid, couponid, leverid, stockid, ptype, price, count = self.get_argument('uid'), self.get_argument('cid'), self.get_argument('lid'), \
                                                                  self.get_argument('stock'), self.get_argument('ptype'), self.get_argument('price'), \
                                                                  self.get_argument('count')

        # init trade model
        tradeModel = models.trade.TradeModel(self.db)

        # check arguments #
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

        # check lever
        lever = tradeModel.getlever(leverid)
        if lever is None:
            raise error.lever_not_exist

        if lever['disable']:
            raise error.lever_has_disabled

        # check coupon
        self.write(protocol.success())
