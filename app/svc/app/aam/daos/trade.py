import time
from web import dao
from app.util import rand
from app.aam import suite, models

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
        self.execute(sql, (suite.enum.coupon.used.code, int(time.time()), couponid))

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
        self.execute(sql, (userid, stockid, couponid, code, ptype, price, count, margin, suite.enum.trade.tobuy.code, int(time.time())))

    def add_order(self, trade, account, stock, otype, ptype, oprice, ocount, operator):
        """
            add new trade order
        :param trade:
        :param account:
        :param stock:
        :param otype:
        :param ptype:
        :param ocount:
        :param oprice:
        :return:
        """
        # insert query
        sql = '''
                insert into tb_trade_order(trade_id, account_id, stock_id, otype, ptype, oprice, ocount, otime, status, slog)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        #prepare status & status log
        otime = int(time.time())
        status_code, status_name = suite.enum.order.notsend.code, suite.enum.order.notsend.name
        logobj = [suite.status.format(operator, suite.enum.otype.buy.name, '', status_name, otime)]
        slog = suite.status.dumps(logobj)

        # execute insert
        self.execute(sql, (trade, account, stock, otype, ptype, oprice, ocount, otime, status_code, slog))

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

    def sell_stock(self, tradeid, count):
        """
            sell stock of specified trade with count
        :param tradeid:
        :param count:
        :return:
        """
        # update query
        sql = '''
                update tb_user_trade
                set fcount = fcount-%s
                where id=%s
            '''

        # execute update
        self.execute(sql, (count, tradeid))
