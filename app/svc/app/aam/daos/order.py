"""
    order dao
"""

from venus import dao

from .. import models, suite
from venus import sqlhelper


class OrderDao(dao.Dao):
    def get(self, **conds):
        """
            get trade order by id
        :param id:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.TradeOrder.fields).table('tb_trade_order').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.TradeOrder(**results[0])

        return None

    def list(self, **conds):
        """
            get trade order by id
        :param id:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.TradeOrder.fields).table('tb_trade_order').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())

        return results

    def add(self, account, scode, sname, tcode, otype, optype, oprice, ocount, otime, odate, callback, slog):
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
                insert into tb_trade_order(account, scode, sname, tcode, otype, optype, oprice, ocount, otime, odate, status, slog, callback, ctime, utime)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        # execute insert
        return self.execute(sql, (account, scode, sname, tcode, otype, optype, oprice, ocount, otime,  odate, suite.enum.order.notsend.code, slog, callback, otime, otime))

    def update(self, orderid, **cvals):
        """
            update order
        :param orderid:
        :param cvals:
        :return:
        """
        # update query
        q = sqlhelper.update().table('tb_trade_order').set(**cvals).where(id=orderid)

        # execute sql
        return self.execute(q.sql(), q.args())
