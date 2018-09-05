"""
    order dao
"""
import time
from web import dao, sqlhelper
from app.aam import models, suite


class OrderDao(dao.Dao):
    def get_order(self, **conds):
        """
            get trade order by id
        :param id:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.TradeOrder.fields).tables('tb_trade_order').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.TradeOrder(**results[0])

        return None

    def add_order(self, trade, account, stock, otype, ptype, oprice, ocount, operator, action):
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
                insert into tb_trade_order(trade_id, account_id, stock_id, otype, ptype, oprice, ocount, otime, status, slog, utime)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        #prepare status & status log
        otime = int(time.time())
        logobj = [suite.status.format(operator, action, '', suite.enum.order.notsend.name, otime)]
        slog = suite.status.dumps(logobj)

        # execute insert
        self.execute(sql, (trade, account, stock, otype, ptype, oprice, ocount, otime, suite.enum.order.notsend.code, slog, otime))


    def update_order(self, orderid, **cvals):
        """
            update order
        :param orderid:
        :param cvals:
        :return:
        """
        # update query
        q = sqlhelper.update().table('tb_trade_order').set(**cvals).where(id=orderid)

        # execute sql
        self.execute(q.sql(), q.args())
