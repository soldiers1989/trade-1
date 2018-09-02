import time
from web import dao


class TradeDao(dao.Dao):
    def add_margin(self, tradeid, money, item):
        """
            add margin
        :return:
        """
        # insert query
        sql = '''
                insert into tb_trade_margin(trade_id, money, item, ctime)
                values(%s, %s, %s, %s)
            '''

        # execute insert
        self.execute(sql, (tradeid, money, item, int(time.time())))

    def add_fee(self, tradeid, item, nmoney, amoney, detail):
        """
            add fee
        :return:
        """
        # insert query
        sql = '''
                insert into tb_trade_fee(trade_id, item, nmoney, amoney, detail, ctime)
                values(%s, %s, %s, %s, %s, %s)
            '''

        # execute insert
        self.execute(sql, (tradeid, item, nmoney, amoney, detail, int(time.time())))

    def add_trade(self, userid, stockid, couponid, code, ptype, price, count, margin, ofee):
        """
            add user trade order
        :param userid:
        :param stockid:
        :param couponid:
        :param code:
        :param ptype:
        :param price:
        :param count:
        :return:
        """
        # insert query
        sql = '''
                insert into tb_user_trade(user_id, stock_id, coupon_id, code, ptype, price, count, margin, ofee, status, ctime)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        # execute insert
        self.execute(sql, (userid, stockid, couponid, code, ptype, price, count, margin, ofee, 'tobuy',int(time.time())))

    def add_lever(self, tradeid, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax):
        """
            add lever of trade
        :return:
        """
        # insert query
        sql = '''
                insert into tb_trade_lever(trade_id, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax)
                values(%s, %s, %s, %s, %s, %s)
            '''

        # execute insert
        self.execute(sql, (tradeid, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax))
