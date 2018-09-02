import time
from web import dao


class TradeDao(dao.Dao):
    def useCounpon(self, couponid):
        """
            use coupon
        :param couponid:
        :return:
        """
        # update query
        sql = '''
                update tb_coupon
                set status=%s, utime=%s
                where id=%s
            '''

        # execute update
        self.execute(sql, ('used', int(time.time()), couponid))

    def useMoney(self, userid, money):
        """
            use money of user
        :param userid:
        :param money:
        :return:
        """
        pass

    def addBill(self, money, item, detail):
        """
            add bill record
        :param money:
        :param item:
        :param detail:
        :return:
        """
        pass

    def addMargin(self, tradeid, money, item):
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

    def addFee(self, tradeid, item, nmoney, amoney, detail):
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

    def addTrade(self, userid, stockid, couponid, code, ptype, price, count, margin, ofee):
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

    def addLever(self, tradeid, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax):
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
