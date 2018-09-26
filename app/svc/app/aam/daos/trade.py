import time

from tlib import rand
from tlib.web import dao
from tlib.web import sqlhelper
from .. import suite, models


class TradeDao(dao.Dao):
    def get_trade(self, **conds):
        """
            get trade record by conditions
        :return:
            None, or first matched trade object
        """
        # select query
        q = sqlhelper.select().columns(*models.UserTrade.fields).table('tb_user_trade').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.UserTrade(**results[0])

        return None

    def get_trades(self, **conds):
        """
            get trade record by conditions
        :return:
            None, or first matched trade object
        """
        # select query
        q = sqlhelper.select().columns(*models.UserTrade.fields).table('tb_user_trade').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())

        return results

    def use_counpon(self, couponid):
        """
            use coupon
        :param couponid:
        :return:
        """
        # update query
        sql = '''
                update tb_user_coupon
                set status=%s, utime=%s
                where id=%s
            '''

        # execute update
        self.execute(sql, (suite.enum.coupon.used.code, int(time.time()), couponid))

    def update_money(self, userid, money):
        """
            use money of user
        :param userid:
        :param money:
        :return:
        """
        # update query
        sql = '''
                update tb_user
                set money = %s
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
                insert into tb_user_trade(user_id, stock_id, coupon_id, code, optype, oprice, ocount, margin, status, ctime, utime, obtime)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        timenow = int(time.time())
        # execute insert
        self.execute(sql, (userid, stockid, couponid, code, ptype, price, count, margin, suite.enum.trade.tobuy.code, timenow, timenow, timenow))

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

    def get_lever(self, tradeid):
        """
            get lever of trade
        :param tradeid:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.TradeLever.fields).table('tb_trade_lever').where(trade_id=tradeid)

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.TradeLever(**results[0])

        return None

    def update_trade(self, tradeid, **cvals):
        """
            update trade
        :param tradeid:
        :param cvals:
        :return:
        """
        # update query
        q = sqlhelper.update().table('tb_user_trade').set(**cvals).where(id=tradeid)

        # execute sql
        self.execute(q.sql(), q.args())
