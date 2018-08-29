import time
from app.aam import model


class TradeModel(model.Model):
    """
        trade model
    """
    def getuser(self, userid):
        """
            get stock
        :param user:
        :return:
        """
        # select query
        sql = '''
                select id, user, pwd, phone, money, disable, ctime, ltime
                from tb_user
                where id = %s
            '''

        # execute query
        results = self.dbselect(sql, (userid,))
        if len(results) > 0:
            return results[0]

        return None

    def getstock(self, stockid):
        """
            get stock
        :param user:
        :return:
        """
        # select query
        sql = '''
                select id, name, jianpin, quanpin, status, `limit`, ctime, mtime
                from tb_stock
                where id = %s
            '''

        # execute query
        results = self.dbselect(sql, (stockid,))
        if len(results) > 0:
            return results[0]

        return None

    def getlever(self, leverid):
        """
            get lever
        :param leverid:
        :return:
        """
        # select query
        sql = '''
                select id, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax, `order`, disable, ctime, mtime
                from tb_lever
                where id = %s
            '''

        # execute query
        results = self.dbselect(sql, (leverid,))
        if len(results) > 0:
            return results[0]

        return None

    def getcoupon(self, couponid):
        """
            get coupon
        :param couponid:
        :return:
        """
        # select query
        sql = '''
                select id, user_id, name, money, status, sdate, edate, ctime, utime
                from tb_user_coupon
                where id = %s
            '''

        # execute query
        results = self.dbselect(sql, (couponid,))
        if len(results) > 0:
            return results[0]

        return None

    def usecoupon(self, couponid):
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
        self.dbexecute(sql, ('used', int(time.time()), couponid))

    def addmargin(self, tradeid, money, item):
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
        self.dbexecute(sql, (tradeid, money, item, int(time.time())))

    def addfee(self, tradeid, item, nmoney, amoney, detail):
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
        self.dbexecute(sql, (tradeid, item, nmoney, amoney, int(time.time())))

    def addtrade(self, userid, stockid, couponid, code, ptype, price, count, margin, ofee):
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
        self.dbexecute(sql, (userid, stockid, couponid, code, ptype, price, count, margin, ofee, 'tobuy',int(time.time())))

    def addlever(self, tradeid, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax):
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
        self.dbexecute(sql, (tradeid, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax))
