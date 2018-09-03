import time
from web import dao
from app.util import rand
from app.aam import enum, models

class TradeDao(dao.Dao):
    def get_by_id(self, id):
        """
            get trade record by id
        :return:
        """
        # select query
        sql = '''
                select id, user_id, stock_id, coupon_id, account_id, code, ptype, oprice, ocount, hprice, hcount, fcount, bprice, bcount, sprice, scount, margin, ofee, ddays, dfee, tprofit, sprofit, status, ctime, ftime
                from tb_user_trade
                where id = %s
            '''

        # execute query
        results = self.select(sql, (id,))
        if len(results) > 0:
            return models.UserTrade(**results[0])

        return None

    def get_by_code(self, code):
        """
            get trade record by code
        :param code:
        :return:
        """
        # select query
        sql = '''
                select id, user_id, stock_id, coupon_id, account_id, code, ptype, oprice, ocount, hprice, hcount, fcount, bprice, bcount, sprice, scount, margin, ofee, ddays, dfee, tprofit, sprofit, status, ctime, ftime
                from tb_user_trade
                where code = %s
            '''

        # execute query
        results = self.select(sql, (code,))
        if len(results) > 0:
            return models.UserTrade(**results[0])

        return None


    def use_counpon(self, couponid):
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
        self.execute(sql, (enum.coupon.used.code, int(time.time()), couponid))

    def use_money(self, userid, money):
        """
            use money of user
        :param userid:
        :param money:
        :return:
        """
        # update query
        sql = '''
                update tb_user
                set money = money-%s
                where id=%s
            '''

        # execute update
        self.execute(sql, (money, userid))

    def add_bill(self, userid, bmoney, lmoney, money, item, detail):
        """
            add bill record
        :param money:
        :param item:
        :param detail:
        :return:
        """
        # insert query
        sql = '''
                insert into tb_user_bill(user_id, code, item, detail, money, bmoney, lmoney, ctime)
                values(%s, %s, %s, %s, %s, %s, %s, %s)
            '''

        # generate code
        code = rand.uuid()

        # execute insert
        self.execute(sql, (userid, code, item, detail, money, bmoney, lmoney, int(time.time())))

    def add_margin(self, tradeid, money, item, detail):
        """
            add margin
        :return:
        """
        # insert query
        sql = '''
                insert into tb_trade_margin(trade_id, `money`, `item`, `detail`, ctime)
                values(%s, %s, %s, %s, %s)
            '''

        # execute insert
        self.execute(sql, (tradeid, money, item, detail, int(time.time())))

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

    def add_trade(self, userid, stockid, couponid, code, ptype, price, count, margin):
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
                insert into tb_user_trade(user_id, stock_id, coupon_id, code, ptype, oprice, ocount, margin, status, ctime)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        # execute insert
        self.execute(sql, (userid, stockid, couponid, code, ptype, price, count, margin, enum.trade.tobuy.code, int(time.time())))

    def add_lever(self, tradeid, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax):
        """
            add lever of trade
        :return:
        """
        # insert query
        sql = '''
                insert into tb_trade_lever(trade_id, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        # execute insert
        self.execute(sql, (tradeid, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax))
